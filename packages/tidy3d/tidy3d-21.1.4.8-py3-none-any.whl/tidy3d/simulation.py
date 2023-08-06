import numpy as np
import json
import h5py
import logging

from .utils import listify, list2str, object_name, cs2span, log_and_raise
from .utils.geom import inside_box_coords
from .utils.log import Tidy3DError, DivergenceError, MonitorError, SourceError
from .utils.check import check_3D_lists
from .constants import int_, float_, complex_, fp_eps, C_0, pec_eps, pmc_eps

from .grid import Grid
from .structure import Structure, Box
from .material import Medium
from . import PEC, PMC

from .source import Source, ModeSource, SourceData
from .monitor import Monitor, TimeMonitor, FreqMonitor, ModeMonitor
from .monitor import MonitorData

from .json_ops import write_parameters, write_structures, write_sources
from .json_ops import write_monitors

class Simulation(object):
    """
    Main class for building a simulation model.
    """
    from .utils.check import _check_size, _check_monitor_size, _check_outside
    from .source._simulation import _compute_modes_source, _src_data
    from .source._simulation import set_mode, spectrum
    from .monitor._simulation import _compute_modes_monitor, _mnt_data
    from .monitor._simulation import data, poynting, flux, decompose
    from .json_ops import _read_simulation
    from .viz import _fmonitors_png, _structure_png
    from .viz import viz_eps_2D, viz_mat_2D, viz_field_2D, viz_modes
    from .viz import viz_source, viz_source_spectrum, viz_source_time

    def __init__(self,
                size,
                center=(0., 0., 0.),
                resolution=None,
                mesh_step=None,
                structures=None,
                sources=None,
                monitors=None,
                symmetries=(0, 0, 0),
                pml_layers=(0, 0, 0),
                run_time=0.,
                courant=0.9
                ):
        """Construct.

        Parameters
        ----------
        center : array_like, optional
            (micron) 3D vector defining the center of the simulation domain.
        size : array_like, optional
            (micron) 3D vector defining the size of the simulation domain.
        resolution : float or array_like, optional
            (1/micron) Number of grid points per micron, or a 3D vector 
            defining the number of grid points per mircon in x, y, and z.
        mesh_step : float or array_like, optional
            (micron) Step size in all directions, or a 3D vector defining the 
            step size in x, y, and z seprately. If provided, ``mesh_step`` 
            overrides the ``resolution`` parameter, otherwise 
            ``mesh_step = 1/resolution``.
        structures : Structure or List[Structure], optional
            Empty list (default) means vacuum. 
        sources : Source or List[Source], optional
            Source(s) to be added to the simulation.
        monitors : Monitor or List[Monitor], optional
            Monitor(s) to be added to the simulation.
        symmetries : array_like, optional
            Array of three integers defining reflection symmetry across a 
            plane bisecting the simulation domain normal to the x-, y-, and 
            z-axis, respectively. Each element can be ``0`` (no symmetry), 
            ``1`` (even, i.e. 'PMC' symmetry) or ``-1`` (odd, i.e. 'PEC' 
            symmetry). Note that the vectorial nature of the fields must be 
            taken into account to correctly determine the symmetry value.
        pml_layers : array_like, optional
            Array of three integers defining the number of PML layers on both 
            sides of the simulation domain along x, y, and z. When set to 
            ``0`` (default), periodic boundary conditions are applied.
        run_time : float, optional
            (second) Total electromagnetic evolution time.
        courant : float, optional
            Courant stability factor, must be smaller than 1, or more 
            generally smaller than the smallest refractive index in the 
            simulation.
        """

        check_3D_lists(center=listify(center), size=listify(size),
                            symmetries=listify(symmetries),
                            pml_layers=listify(pml_layers))

        logging.info("Initializing simulation...")

        # Set PML size. Npml defines the number of layers on all 6 sides.
        self.pml_layers = listify(pml_layers)
        self.Npml = np.vstack((pml_layers, pml_layers)).astype(int_).T

        # Set spatial mesh step
        if mesh_step is None:
            if resolution is None:
                log_and_raise(
                    "Either 'mesh_step' or 'resolution' must be set.",
                    ValueError
                )
            mesh_step = 1/np.array(resolution)
        else:
            if resolution is not None:
                logging.info(
                    "Note: parameter 'mesh_step' overrides 'resolution'."
                    )

        # Set simulation size inside the PML and including the PML
        self.center = np.array(center, dtype=float_)
        self.size_in = np.array(size, dtype=float_)
        self.size = self.size_in + 2*np.array(pml_layers)*mesh_step
        self.span = cs2span(self.center, self.size)

        # Initialize grid
        self.grid = Grid(self.span, mesh_step, symmetries, courant)

        logging.info(
            f"Mesh step (micron): {list2str(self.grid.mesh_step, '%1.2e')}.\n"
            "Simulation domain in number of grid points: "
            f"{list2str(self.grid.Nxyz, '%d')}."
            )

        # Computational domain including symmetries, if any
        self.span_sym = np.copy(self.span)
        self.Nxyz_sym = np.copy(self.grid.Nxyz)
        for d, sym in enumerate(symmetries):
            if sym==-1:
                self.span_sym[d, 0] += self.size[d]/2
                self.Nxyz_sym[d] = self.Nxyz_sym[d]//2
            elif sym==1:
                self.span_sym[d, 0] += self.size[d]/2 - self.grid.mesh_step[d]
                self.span_sym[d, 1] += self.grid.mesh_step[d]
                self.Nxyz_sym[d] = self.Nxyz_sym[d]//2 + 2
        # Print new size, if there are any symmetries
        if np.any(np.array(symmetries)!=0):
            logging.info(
                "Computation domain (after symmetries): "
                f"{list2str(self.Nxyz_sym, '%d')}."
            )
        # Total number of points in computational domain (after symmetries)
        self.Np = np.prod(self.Nxyz_sym)
        logging.info(
            f"Total number of grid points: {self.Np:.2e}."
        )

        # Set up run time
        self.set_time(run_time, courant)
        logging.info(f"Total number of time steps: {self.Nt}.")
        if self.Nt <= 0:
            logging.warning(
                f"run_time = {self.run_time:.2e} smaller than a single "
                f"simulation time step dt = {self.grid.dt:.2e}.",
            )

        # Check the simulation size
        self._check_size()

        # Materials and indexing populated when adding ``Structure`` objects.
        self._mat_inds = [] # material index of each structure
        self._materials = [] # list of materials included in the simulation
        self._structures = []
        self._str_names = [] # structure names in the simulation
        self._mat_names = [] # material names in the simulation

        # List containing SourceData for all sources, and a dictionary 
        # used to get SourceData from id(source), e.g. src_data = 
        # self._source_ids[id(source)]
        self._source_data = []
        self._source_ids = {}

        # List containing MonitorData for all monitors, and a dictionary 
        # used to get MonitorData from id(monitor)
        self._monitor_data = []
        self._monitor_ids = {}

        # Structures and material indexing for symmetry boxes
        self._structures_sym = [] # PEC/PMC boxes added for symmetry

        # Add structures, sources, monitors, symmetries
        if structures:
            self.add(structures)
        if sources:
            self.add(sources)
        if monitors:
            self.add(monitors)
        self._add_symmetries(symmetries)

        # JSON file from which the simulation is loaded
        self.fjson = None

    def __repr__(self):
        rep = "Tidy3D Simulation:\n"
        rep += "center      = %s\n" % list2str(self.center, "%1.4f")
        rep += "size        = %s\n" % list2str(self.size_in, "%1.4f")
        rep += "size w. pml = %s\n" % list2str(self.size, "%1.4f")
        rep += "mesh_step   = %s\n" % list2str(self.grid.mesh_step, "%1.4f")
        rep += "run_time    = %1.2e\n"%self.run_time
        rep += "symmetries  = %s\n" % list2str(self.symmetries, "%d")
        rep += "pml_layers  = %s\n\n" % list2str(self.pml_layers, "%d")

        rep += "Number of grid points in x, y, z: %s\n" % list2str(
                    self.grid.Nxyz, "%d")
        rep += "    after symmeries             : %s\n"%list2str(
                    self.Nxyz_sym, "%d")
        rep += "Total number of grid points: %d\n" % np.prod(self.grid.Nxyz)
        rep += "    after symmetries:        %d\n" % self.Np

        rep += "Number of time steps       : %d\n" % self.Nt
        rep += "Number of structures       : %d\n"%len(self._structures)
        rep += "Number of sources          : %d\n"%len(self.sources)
        rep += "Number of monitors         : %d\n"%len(self.monitors)

        return rep

    @property
    def materials(self):
        """ List containing all materials included in the simulation."""
        return self._materials

    @property
    def mat_inds(self):
        """ List containing the material index in :attr:`.materials` of every 
        structure in :attr:`.structures`. """
        return self._mat_inds

    @property
    def structures(self, sym=None):
        """ List containing all :class:`Structure` objects. """
        return self._structures

    @structures.setter
    def structures(self, new_struct):
        raise RuntimeError("Structures can be added upon Simulation init, "
                            "or using 'Simulation.add()'")

    @property
    def sources(self):
        """ List containing all :class:`Source` objects. """
        return [src_data.source for src_data in self._source_data]

    @sources.setter
    def sources(self, new_sources):
        raise RuntimeError("Sources can be added upon Simulation init, "
                            "or using 'Simulation.add()'")

    @property
    def monitors(self):
        """ List containing all :class:`.Monitor` objects. """
        return [mnt_data.monitor for mnt_data in self._monitor_data]

    @monitors.setter
    def monitors(self, new_monitors):
        raise RuntimeError("Monitors can be added upon Simulation init, "
                            "or using 'Simulation.add()'")

    def _add_structure(self, structure):
        """ Adds a Structure object to the list of structures and to the 
        permittivity array. """
        self._structures.append(structure)
        name = object_name(self._str_names, structure, "struct")
        self._str_names.append(name)

        try:
            mind = self.materials.index(structure.material)
            self._mat_inds.append(mind)
        except ValueError:
            if len(self.materials) < 200:
                mat = structure.material
                self._materials.append(mat)
                name = object_name(self._mat_names, mat, "mat")
                self._mat_names.append(name)
                self._mat_inds.append(len(self.materials)-1)
            else:
                log_and_raise(
                    "Maximum 200 distinct materials allowed.",
                    RuntimeError
                )

    def _add_source(self, source):
        """ Adds a Source object to the list of sources.
        """

        if id(source) in self._source_ids.keys():
            logging.warning("Source already in Simulation, skipping.")
            return

        src_data = SourceData(source)
        name_list = [s.name for s in self._source_data]
        src_data.name = object_name(name_list, source, 'source')
        self._check_outside(source, src_data.name)
        src_data._mesh_norm(self.grid.mesh_step)
        src_data._set_tdep(self.grid.tmesh)
        self._source_data.append(src_data)
        self._source_ids[id(source)] = src_data

        if isinstance(source, ModeSource):
            try:
                # Set the frequencies in the mode plane and compute the 
                # eps array in the plane at every frequency
                freq = source.source_time.frequency
                src_data.mode_plane._set_eps(self, freq)
            except Tidy3DError as e:
                log_and_raise(
                    "Unable to set mode source. " + str(e), SourceError
                )

    def _add_monitor(self, monitor):
        """ Adds a time or frequency domain Monitor object to the 
        corresponding list of monitors.
        """

        if id(monitor) in self._monitor_ids.keys():
            logging.warning("Monitor already in Simulation, skipping.")
            return

        mnt_data = MonitorData(monitor)
        name_list = [m.name for m in self._monitor_data]
        mnt_data.name = object_name(name_list, monitor, 'monitor')
        self._check_outside(monitor, mnt_data.name)
        self._monitor_data.append(mnt_data)
        self._monitor_ids[id(monitor)] = mnt_data

        if isinstance(monitor, TimeMonitor):
            mnt_data._set_tmesh(self.grid.tmesh)

        memGB = self._check_monitor_size(monitor)
        logging.info(
            f"Estimated data size (GB) of monitor {mnt_data.name}: "
            f"{memGB:.4f}."
        )

        # Initialize the ModePlane of a ModeMonitor
        if isinstance(monitor, ModeMonitor):
            try:
                mnt_data.mode_plane._set_eps(self, monitor.freqs)
            except Tidy3DError as e:
                log_and_raise(
                    "Unable to set mode monitor. " + str(e), MonitorError
                )

    def _add_symmetries(self, symmetries):
        """ Add all symmetries as PEC or PMC boxes.
        """
        self.symmetries = listify(symmetries)
        for dim, sym in enumerate(symmetries):
            if sym not in [0, -1, 1]:
                log_and_raise(
                    "Reflection symmetry values can be 0 (no symmetry), "
                    "1, or -1.",
                    ValueError
                )
            elif sym==1 or sym==-1:
                sym_cent = np.copy(self.center)
                sym_size = np.copy(self.size)
                sym_cent[dim] -= self.size[dim]/2
                sym_size[dim] = sym_size[dim] + fp_eps
                sym_mat = PEC if sym==-1 else PMC
                sym_pre = 'pec' if sym==-1 else 'pmc'
                self._structures_sym.append(Box(center=sym_cent,
                                                size=sym_size,
                                                material=sym_mat,
                                                name=sym_pre + '_sym%d'%dim))

    def _pml_config(self):
        """Set the CPML parameters. Default configuration is hard-coded. This 
        could eventually be exposed to the user, or, better, named PML 
        profiles can be created.
        """
        cfs_config = {'sorder': 3, 'smin': 0., 'smax': None, 
                    'korder': 3, 'kmin': 1., 'kmax': 3., 
                    'aorder': 1, 'amin': 0., 'amax': 0}
        # cfs_config = {'sorder': 3, 'smin': 0., 'smax': None, 
        #             'korder': 3, 'kmin': 1., 'kmax': 1., 
        #             'aorder': 1, 'amin': 0., 'amax': 0.8}
        return cfs_config

    def _get_eps(self, mesh, edges='in', pec_val=pec_eps, pmc_val=pmc_eps,
                    freq=None, syms=True):
        """Compute the permittivity over a given mesh. For large simulations, 
        this could be computationally heavy, so preferably use only over small 
        meshes (e.g. 2D cuts). 
        
        Parameters
        ----------
        mesh : tuple
            Three 1D arrays defining the mesh in x, y, z.
        edges : {'in', 'out', 'average'}
            When an edge of a structure sits exactly on a mesh point, it is 
            counted as in, out, or an average value of in and out is taken.
        pec_val : float
            Value to use for PEC material.
        pmc_val : float
            Value to use for PMC material.
        freq : float or None, optional
            (Hz) frequency at which to query the permittivity. If 
            ``None``, the instantaneous :math:`\\epsilon_\\infty` is returned.
        syms : bool, optional
            If ``True``, PEC/PMC boxes are overlaid as defined by the 
            simulation symmetries.
        
        Returns
        -------
        eps : np.ndarray
            Array of size (mesh[0].size, mesh[1].size, mesh[2].size) defining 
            the (complex) relative permittivity at each point.
        """

        Nx, Ny, Nz = [mesh[i].size for i in range(3)]
        eps = np.ones((Nx, Ny, Nz), dtype=complex_)

        strs = self.structures
        if syms==True:
            strs = strs + self._structures_sym

        # Apply all structures
        for struct in strs:
            eps_val = struct._get_eps_val(pec_val, pmc_val, freq)
            struct._set_val(mesh, eps, eps_val, edges=edges)

        # return eps array after filling in all structures
        return eps

    def _get_mat(self, mesh, edges='in', pec_val=pec_eps, pmc_val=pmc_eps,
                    syms=True):
        """Get the material index over a given mesh. For large simulations, 
        this could be computationally heavy, so preferably use only over small 
        meshes (e.g. 2D cuts). 
        
        Parameters
        ----------
        mesh : tuple
            Three 1D arrays defining the mesh in x, y, z.
        edges : {'in', 'out', 'average'}
            When an edge of a structure sits exactly on a mesh point, it is 
            counted as in, out, or an average value of in and out is taken.
        pec_val : float
            Value to use for PEC material.
        pmc_val : float
            Value to use for PMC material.
        syms : bool, optional
            If ``True``, PEC/PMC boxes are overlaid as defined by the 
            simulation symmetries.
        
        Returns
        -------
        mat_inds : np.ndarray
            Array of size (mesh[0].size, mesh[1].size, mesh[2].size) defining 
            the index in the list of materials of the material at each point.
        """

        Nx, Ny, Nz = [mesh[i].size for i in range(3)]
        # Denote vacuum as -1
        mat_inds = -np.ones((Nx, Ny, Nz), dtype=int_)

        strs = self.structures
        if syms==True:
            strs = strs + self._structures_sym

        # Apply all structures
        for (istruct, struct) in enumerate(strs):
            
            # Use the get_eps function to check if PEC/PMC
            mat_ind = struct._get_eps_val(pec_val, pmc_val)
            if mat_ind not in [pec_val, pmc_val]:
                mat_ind = self.mat_inds[istruct]
            
            struct._set_val(mesh, mat_inds, mat_ind, edges=edges)

        # return material index array after filling in all structures
        return mat_inds

    def add(self, objects):
        """Add a list of objects, which can contain structures, sources, and 
        monitors.
        """

        for obj in listify(objects):
            if isinstance(obj, Structure):
                self._add_structure(obj)
            elif isinstance(obj, Source):
                self._add_source(obj)
            elif isinstance(obj, Monitor):
                self._add_monitor(obj)

    def epsilon(self, monitor=None, center=(0., 0., 0.), size=(0., 0., 0.),
                pec_val=pec_eps, pmc_val=pmc_eps, frequency=None, syms=True):
        """Compute the complex relative permittivity inside a volume. The 
        permittivity is returned at the Yee grid centers isnide the volume.
        For large simulations, this could be computationally heavy over the
        full simulation volume, so this function is ideally used over a
        sub-domain, e.g. a 2D cut. The volume ``size`` can be ``0`` in any
        dimension, in which case the single Yee grid center closest to the
        volume ``center`` in that dimension is taken.
        
        Parameters
        ----------
        monitor : None or Monitor, optional
            If provided, overrides ``center`` and ``size``, and the monitor 
            volume is used.
        center : array_like, optional
            (micron) 3D vector defining the center of the queried volume.
        size : array_like, optional
            (micron) 3D vector defining the size of the queried volume.
        pec_val : float
            Value to use for PEC material. Default is ``1e-6``.
        pmc_val : float
            Value to use for PMC material. Default is ``3e-6``.
        frequency : float or None, optional
            (Hz) frequency at which to query the permittivity. If 
            ``None``, the instantaneous :math:`\\epsilon_\\infty` is returned.
        syms : bool, optional
            If ``True``, PEC/PMC boxes are overlaid as defined by the 
            simulation symmetries, with values defined by ``pec_val`` and 
            ``pmc_val``.
        
        Returns
        -------
        epsilon : np.ndarray
            Array defining the (complex) relative permittivity at the center 
            of each Yee cell inside the volume.
        mesh : tuple of np.ndarray
            Three arrays defining the Cartesian grid of x, y, and z positions
            where the permittivity array is returned, such that
            ``epsilon.shape == (mesh[0].size, mesh[1].size, mesh[2].size)``.
        """

        if monitor is not None:
            span = monitor.span
        else:
            span = cs2span(center, size)

        minds = inside_box_coords(span, self.grid.coords)
        mesh = (
            self.grid.mesh[0][minds[0][0]:minds[0][1]],
            self.grid.mesh[1][minds[1][0]:minds[1][1]],
            self.grid.mesh[2][minds[2][0]:minds[2][1]],
        )

        eps = self._get_eps(mesh, pec_val=pec_val, pmc_val=pmc_val,
                    freq=frequency, syms=syms)

        return eps, mesh


    def set_time(self, run_time=None, courant=None):
        """Change the value of the run time of the simulation and the time 
        step determined by the courant stability factor.
        
        Parameters
        ----------
        run_time : None or float
            (second) If a float, the new ``run_time`` of the simulation. 
        courant : None or float, optional
            If a float, the new courant factor to be used.
        """

        if run_time is not None:
            self.run_time = run_time

        if courant is not None:
            self.courant = courant
            self.grid.set_time_step(courant)

        # Raise an error if number of time steps is crazy large
        if self.run_time/self.grid.dt > 1e9:
            log_and_raise(
                f"Too many time steps, {self.run_time/self.grid.dt:1.2e}.",
                ValueError
            )

        if run_time is not None or courant is not None:
            self.grid.set_tmesh(self.run_time)
            self.Nt = np.array(self.grid.tmesh.size)

            # Update all sources that are already in the simulation
            try:
                for src_data in self._source_data:
                    src_data._set_tdep(self.grid.tmesh)
            except AttributeError:
                pass


    def compute_modes(self, mode_object, Nmodes):
        """Compute the eigenmodes of the 2D cross-section of a 
        :class:`.ModeSource` or :class:`.ModeMonitor` object, assuming 
        translational invariance in the third dimension. The eigenmodes are 
        computed in decreasing order of propagation constant, at the central 
        frequency of the :class:`.ModeSource` or for every frequency in the 
        list of frequencies of the :class:`.ModeMonitor`. In-plane, periodic 
        boundary conditions are assumed, such that the mode shold decay at the 
        boundaries, or be matched with periodic boundary conditions in the 
        simulation. Use :meth:`.viz_modes` to visuzlize the computed 
        eigenmodes.
        
        Parameters
        ----------
        mode_object : ModeSource or ModeMonitor
            The object defining the 2D plane in which to compute the modes.
        Nmodes : int
            Number of eigenmodes to compute.
        """

        if isinstance(mode_object, Monitor):
            try:
                self._compute_modes_monitor(mode_object, Nmodes)
            except Tidy3DError as e:
                log_and_raise(
                    "Unable to compute modes of monitor. " + str(e),
                    MonitorError
                )

        elif isinstance(mode_object, Source):
            try:
                self._compute_modes_source(mode_object, Nmodes)
            except Tidy3DError as e:
                log_and_raise(
                    "Unable to compute modes of source. " + str(e),
                    SourceError
                )

    def export(self):
        """Return a dictionary with all simulation parameters and objects.
        """
        js = {}
        js["parameters"] = write_parameters(self)
        js["sources"] = write_sources(self)
        js["monitors"] = write_monitors(self)
        js["materials"], js["structures"] = write_structures(self)

        return js

    def export_json(self, fjson):
        """Export the simulation specification to a JSON file.
        
        Parameters
        ----------
        fjson : str
            JSON file name.
        """

        self.fjson = fjson
        with open(fjson, 'w') as json_file:
            json.dump(self.export(), json_file, indent=4)

    @classmethod
    def import_json(cls, fjson):
        """Import a simulation specification from a JSON file.
        
        Parameters
        ----------
        fjson : str
            JSON file name.
        """
        
        with open(fjson, 'r') as json_file:
            js = json.load(json_file)

        sim = cls._read_simulation(js)
        sim.fjson = fjson

        return sim

    def load_results(self, dfile, ind_src_norm=0):
        """Load all monitor data recorded from a Tidy3D run.
        The data from each monitor can then be queried using 
        :meth:`.data`.
        
        Parameters
        ----------
        dfile : str
            Path to the file containing the simulation results.
        ind_src_norm : int or None, optional
            Index of which source to be used for normalization of frequency 
            monitors. If ``None`` or larger than the number of monitors in the 
            simulation, the raw field data is loaded.
        """

        mfile = h5py.File(dfile, "r")

        if "diverged" in mfile.keys():
            if mfile["diverged"][0] == 1:
                log_and_raise(mfile["diverged_msg"][0], DivergenceError)

        if len(self.sources) <= ind_src_norm:
            logging.warning(
                "Soure normalization index larger than number of sources "
                "in the simulation; no normalization applied."
            )
        elif ind_src_norm is not None:
            logging.info(
                "Applying source normalization to all frequency "
                f"monitors using source index {ind_src_norm}."
            )

        for (im, mnt_data) in enumerate(self._monitor_data):
            # Set source normalization
            if isinstance(mnt_data.monitor, FreqMonitor):
                if ind_src_norm is None or len(self.sources) <= ind_src_norm:
                    mnt_data.set_source_norm(None)
                else:
                    src_data = self._source_data[ind_src_norm]
                    mnt_data.set_source_norm(src_data)

            # Load data
            mname = mnt_data.name
            mnt_data._load_fields(mfile[mname]["indspan"][0, :],
                            mfile[mname]["indspan"][1, :],
                            np.array(mfile[mname]["E"]),
                            np.array(mfile[mname]["H"]), 
                            self.symmetries, self.grid.Nxyz)
            mnt_data.xmesh = np.array(mfile[mname]["xmesh"])
            mnt_data.ymesh = np.array(mfile[mname]["ymesh"])
            mnt_data.zmesh = np.array(mfile[mname]["zmesh"])
            mnt_data.mesh_step = self.grid.mesh_step

        mfile.close()