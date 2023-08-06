import numpy as np

from .structure import Box, Sphere, Cylinder, PolySlab, GdsSlab
from .source import VolumeSource, PointDipole, PlaneSource, PlaneWave, \
                    ModeSource, GaussianPulse
from .monitor import TimeMonitor, FreqMonitor, ModeMonitor
from .material import Medium, PEC, PMC
from .dispersion import DispersionModel
from .utils import listify, span2cs, cs2span, log_and_raise

def write_parameters(sim):
    """ Convert simulation parameters to a dict.
    """
    cent = sim.center
    # We only specify the size inside the pml when initializing simulation
    size = sim.size_in
    
    # Compute-weight prefactor per 1 billion (grid points * time steps)
    compute_factor = 0.5

    parameters = {
                "unit_length": "um",
                "unit_frequency": "THz",
                "unit_time": "ps",
                "x_cent": float(cent[0]),
                "y_cent": float(cent[1]),
                "z_cent": float(cent[2]),
                "x_span": float(size[0]),
                "y_span": float(size[1]),
                "z_span": float(size[2]),
                "mesh_step": sim.grid.mesh_step.tolist(),
                "symmetries": sim.symmetries, 
                "pml_layers": sim.pml_layers,
                "run_time": sim.run_time*1e12,
                "courant": sim.courant,
                "nodes": int(sim.Np),
                "time_steps": int(sim.Nt),
                "compute_weight": float(compute_factor*sim.Np*sim.Nt/1e9)
                }

    return parameters

def write_structures(sim):
    """ Convert all Structure objects to a list of text-defined objects, 
    and all the corresponding Material objects to a list of text-defined 
    materials. 
    """
    mat_list = []
    for (imat, material) in enumerate(sim.materials):
        mat = {"name": sim._mat_names[imat]}
        if isinstance(material, Medium):
            poles = []
            for pole in material.poles:
                poles.append([pole[0].real, pole[0].imag,
                                pole[1].real, pole[1].imag])
            mat.update({"type": "Medium",
                   "permittivity": float(material.eps),
                   "conductivity": float(material.sigma),
                   "poles": poles})
        elif isinstance(material, PEC):
            mat.update({"type": "PEC"})
        elif isinstance(material, PMC):
            mat.update({"type": "PMC"})
        mat_list.append(mat)

    obj_list = []
    for istruct, structure in enumerate(sim.structures):
        obj = {
                "name": sim._str_names[istruct],
                "mat_index": sim.mat_inds[istruct]
                }
        if isinstance(structure, Box):
            cent, size = structure.center, structure.size
            obj.update({"type": "Box",
                        "x_cent": float(cent[0]),
                        "y_cent": float(cent[1]),
                        "z_cent": float(cent[2]),
                        "x_span": float(size[0]),
                        "y_span": float(size[1]),
                        "z_span": float(size[2])})
            obj_list.append(obj)
        elif isinstance(structure, Sphere):
            obj.update({"type": "Sphere",
                        "x_cent": float(structure.center[0]),
                        "y_cent": float(structure.center[1]),
                        "z_cent": float(structure.center[2]),
                        "radius": float(structure.radius)})
            obj_list.append(obj)
        elif isinstance(structure, Cylinder):
            obj.update({"type": "Cylinder",
                        "x_cent": float(structure.center[0]),
                        "y_cent": float(structure.center[1]),
                        "z_cent": float(structure.center[2]),
                        "axis": structure.axis,
                        "radius": float(structure.radius),
                        "height": float(structure.height)})
            obj_list.append(obj)
        elif isinstance(structure, PolySlab):
            obj.update({"type": "PolySlab",
                        "vertices": structure.vertices.tolist(),
                        "z_cent": float(structure.z_cent),
                        "z_size": float(structure.z_size)})
            obj_list.append(obj)

        # Split GdsSlab into PolySlab objects
        if isinstance(structure, GdsSlab):
            for (ip, verts) in enumerate(structure.gds_cell.get_polygons()):
                poly = obj.copy()
                if poly['name'] is None:
                    poly['name'] = 'struct%04d_poly%04d'%(istruct, ip)
                else:
                    poly['name'] += '_poly%04d'%ip
                poly.update({"type": "PolySlab",
                        "vertices": verts.tolist(),
                        "z_cent": float(structure.z_cent),
                        "z_size": float(structure.z_size)})
                obj_list.append(poly)
        
    return mat_list, obj_list

def write_sources(sim):
    src_list = []
    for source in sim.sources:
        src_time = {
            "type": "GaussianPulse",
            "frequency": source.source_time.frequency*1e-12, 
            "fwidth": source.source_time.fwidth*1e-12,
            "offset": source.source_time.offset,
            "phase": source.source_time.phase
            }
        src_data = sim._src_data(source)
        if isinstance(source, VolumeSource):
            src = {
                "name": src_data.name,
                "type": "VolumeSource",
                "source_time": src_time,
                "center": source.center.tolist(),
                "size": source.size.tolist(),
                "component": source.component, 
                "amplitude": float(source.amplitude),
                }
        elif isinstance(source, PointDipole):
            src = {
                "name": src_data.name,
                "type": "PointDipole",
                "source_time": src_time,
                "center": source.center.tolist(),
                "size": source.size.tolist(),
                "component": source.component, 
                "amplitude": float(source.amplitude),
                }
        elif isinstance(source, PlaneWave):
            src = {
                "name": src_data.name,
                "type": "PlaneWave",
                "source_time": src_time,
                "injection_axis": source.injection_axis,
                "position": source.position,
                "polarization": source.polarization,
                "amplitude": float(source.amplitude)
                }
        elif isinstance(source, PlaneSource):
            src = {
                "name": src_data.name,
                "type": "PlaneSource",
                "source_time": src_time,
                "position": source.position,
                "normal": source.normal,
                "direction": source.direction,
                "diff_order": source.diff_order,
                "pol_angle": float(source.pol_angle),
                "polarization": source.polarization.tolist(),
                "amplitude": float(source.amplitude)
                }
        elif isinstance(source, ModeSource):
            mode_ind = src_data.mode_ind
            if mode_ind is None:
                log_and_raise(
                    f"Mode index of source {src_data.name} not yet set, "
                    "use Simulation.set_mode().",
                    RuntimeError
                )
            src = {
                "name": src_data.name,
                "type": "ModeSource",
                "source_time": src_time,
                "center": source.center.tolist(),
                "size": source.size.tolist(),
                "direction": source.direction,
                "amplitude": float(source.amplitude),
                "mode_ind": int(mode_ind)
                }
        src_list.append(src)

    return src_list

def write_monitors(sim):
    mnt_list = []
    for monitor in sim.monitors:
        cent, size = span2cs(monitor.span)
        mnt_data = sim._mnt_data(monitor)
        mnt = {"name": mnt_data.name,
                "x_cent": float(cent[0]),
                "y_cent": float(cent[1]),
                "z_cent": float(cent[2]),
                "x_span": float(size[0]),
                "y_span": float(size[1]),
                "z_span": float(size[2]),
                "field": monitor.field
                }
        if isinstance(monitor, TimeMonitor):
            mnt.update({
                "type": "TimeMonitor",
                "t_start": monitor.t_start,
                "t_stop": monitor.t_stop
                })
        elif isinstance(monitor, ModeMonitor):
            mnt.update({
                "type": "ModeMonitor",
                "frequency": [f*1e-12 for f in monitor.freqs]
                })
        elif isinstance(monitor, FreqMonitor):
            mnt.update({
                "type": "FrequencyMonitor",
                "frequency": [f*1e-12 for f in monitor.freqs]
                })
        mnt_list.append(mnt)

    return mnt_list

def read_structures(sim, js, scale_l=1):
    materials = []
    for mat in js['materials']:
        if mat['type'].lower()=='medium':
            poles = []
            for pole in mat['poles']:
                poles.append((pole[0]+pole[1]*1j, pole[2]+pole[3]*1j))
            if 0 == len(poles):
                materials.append(Medium(
                    epsilon = mat['permittivity'],
                    sigma = mat['conductivity']
                ))
            else:
                materials.append(Medium(
                    epsilon = DispersionModel(
                        eps_inf = mat['permittivity'],
                        poles = poles
                    ),
                    sigma = mat['conductivity']
                ))
        elif mat['type'].lower()=='pec':
            materials.append(PEC())
        elif mat['type'].lower()=='pmc':
            materials.append(PMC())

    for obj in js['structures']:
        if obj['type'].lower()=='box':
            cent = np.array([obj['x_cent'], obj['y_cent'],
                        obj['z_cent']])*scale_l
            size = np.array([obj['x_span'], obj['y_span'],
                        obj['z_span']])*scale_l
            sim.add(Box(center=cent, size=size,
                                material=materials[obj['mat_index']],
                                name=obj['name']))
        elif obj['type'].lower()=='sphere':
            cent = [obj['x_cent'], obj['y_cent'], obj['z_cent']]
            sim.add(Sphere(center=cent, radius=obj['radius'], 
                                material=materials[obj['mat_index']],
                                name=obj['name']))
        elif obj['type'].lower()=='cylinder':
            cent = [obj['x_cent'], obj['y_cent'], obj['z_cent']]
            sim.add(Cylinder(center=cent, axis=obj['axis'], 
                                radius=obj['radius'], height=obj['height'],
                                material=materials[obj['mat_index']],
                                name=obj['name']))
        elif obj['type'].lower()=='polyslab':
            sim.add(PolySlab(vertices=obj['vertices'],
                                z_cent=obj['z_cent'], z_size=obj['z_size'], 
                                material=materials[obj['mat_index']],
                                name=obj['name']))
        else:
            raise NotImplementedError("Unknown structure type " + obj['type'])

def read_sources(sim, js, scale_l=1, scale_f=1):
    sources = []
    js_params = js['parameters']
    for src in js['sources']:
        src_time = src['source_time']
        source_time = GaussianPulse(src_time['frequency']*scale_f, 
                                     src_time['fwidth']*scale_f,
                                     src_time['offset'],
                                     src_time['phase'])
        if src['type'].lower()=='planewave':
            psource = PlaneWave(source_time=source_time,
                            injection_axis=src['injection_axis'].lower(),
                            position=src['position'],
                            polarization=src['polarization'].lower(),
                            amplitude=src['amplitude'],
                            name=src['name'])
            sim.add(psource)
            sim._src_data(psource).mode_ind = 0
        elif src['type'].lower()=='planesource':
            psource = PlaneSource(source_time=source_time,
                            position=src['position'],
                            normal=src['normal'].lower(),
                            direction=src['direction'].lower(),
                            diff_order=src['diff_order'],
                            pol_angle=src['pol_angle'],
                            polarization=src['polarization'],
                            amplitude=src['amplitude'],
                            name=src['name'])
            sim.add(psource)
            sim._src_data(psource).mode_ind = 0
        elif src['type'].lower()=='pointdipole':
            sim.add(PointDipole(
                            source_time=source_time,
                            center=src['center'],
                            component=src['component'],
                            amplitude=src['amplitude'],
                            name=src['name']))
        elif src['type'].lower()=='volumesource':
            sim.add(VolumeSource(
                            source_time=source_time,
                            center=src['center'],
                            size=src['size'], 
                            component=src['component'],
                            amplitude=src['amplitude'],
                            name=src['name']))
        elif src['type'].lower()=='modesource':
            msource = ModeSource(
                            source_time=source_time,
                            center=src['center'],
                            size=src['size'],
                            direction=src['direction'].lower(),
                            amplitude=src['amplitude'],
                            name=src['name'])
            # Overwrite the mode index; this will then ensure that set_mode() 
            # is called when the source is added to a Simulation object.
            sim.add(msource)
            sim._src_data(msource).mode_ind = src['mode_ind']
        else:
            raise NotImplementedError("Unknown source type " + source['type'])

def read_monitors(sim, js, scale_l=1, scale_f=1):
    """ Read monitors from a json dictionary and load them to the Simulation 
    object sim.
    """

    for mnt in js['monitors']:
        cent = np.array([mnt['x_cent'], mnt['y_cent'],
                                mnt['z_cent']])*scale_l
        size = np.array([mnt['x_span'], mnt['y_span'],
                                mnt['z_span']])*scale_l
        if mnt['type'].lower()=='modemonitor':    
            sim.add(ModeMonitor(center=cent, size=size,
                        freqs=[f*scale_f for f in listify(mnt['frequency'])],
                        name=mnt['name']))
        elif mnt['type'].lower()=='frequencymonitor':    
            sim.add(FreqMonitor(center=cent, size=size,
                        freqs=[f*scale_f for f in listify(mnt['frequency'])],
                        field=mnt['field'],
                        name=mnt['name']))
        elif mnt['type'].lower()=='timemonitor':
            sim.add(TimeMonitor(center=cent, size=size,
                        field=mnt['field'],
                        t_start=mnt['t_start'],
                        t_stop=mnt['t_stop'],
                        name=mnt['name']))
        else:
            raise NotImplementedError("Unknown monitor type " + mnt['type'])

@classmethod
def _read_simulation(cls, js: dict):
    """ Initialize Simulation object based on JSON input dictionary ``js``.
    """

    # Unit scalings
    if js['parameters']['unit_length'].lower() == "mm":
        scale_l = 1e3
    elif js['parameters']['unit_length'].lower() == "um":
        scale_l = 1
    elif js['parameters']['unit_length'].lower() == "nm":
        scale_l = 1e-3

    if js['parameters']['unit_frequency'].lower() == "thz":
        scale_f = 1e12
    elif js['parameters']['unit_frequency'].lower() == "ghz":
        scale_f = 1e9
    elif js['parameters']['unit_frequency'].lower() == "mhz":
        scale_f = 1e6

    if js['parameters']['unit_time'].lower() == "fs":
        scale_t = 1e-15
    elif js['parameters']['unit_time'].lower() == "ps":
        scale_t = 1e-12
    elif js['parameters']['unit_time'].lower() == "ns":
        scale_t = 1e-9

    # Parse simulation parameters
    js_params = js['parameters']

    # Simulation span
    sim_cent = np.array([0., 0., 0.])
    if "x_cent" in js_params.keys():
        sim_cent[0] = js_params["x_cent"]*scale_l
    if "y_cent" in js_params.keys():
        sim_cent[1] = js_params["y_cent"]*scale_l
    if "z_cent" in js_params.keys():
        sim_cent[2] = js_params["z_cent"]*scale_l

    sim_size = scale_l*np.array([js_params["x_span"], js_params["y_span"],
                                js_params["z_span"]])

    # Pml size
    pml_layers = np.array([0, 0, 0])
    if "pml_layers" in js_params.keys():
        pml_layers = js_params["pml_layers"]
    else:
        # If pml_layers not set directly, we assume BCs are defined
        for (i, si) in enumerate(['x', 'y', 'z']):
            if js_params[si+'_bc'].lower()=='pml':
                # set some default PML thickness
                pml_layers[i] = 12


    sim_params = {
            'center': sim_cent,
            'size': sim_size, 
            'mesh_step': js_params['mesh_step'],
            'run_time': js_params['run_time']*scale_t,
            'pml_layers': pml_layers
            }

    for key in ['symmetries', 'courant']:
        try:
            sim_params[key] = js_params[key]
        except:
            pass

    sim = cls(**sim_params)

    if "structures" in js.keys():
        read_structures(sim, js, scale_l=scale_l)
    if "sources" in js.keys():
        read_sources(sim, js, scale_l, scale_f)
    if "monitors" in js.keys():
        read_monitors(sim, js, scale_l, scale_f)
        
    return sim