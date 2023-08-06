import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import logging

from ..constants import xyz_dict, xyz_list, fp_eps, pec_eps, pmc_eps
from ..utils import log_and_raise

def _eps_cmap(eps_r, alpha=1, cmap=None, clim=None):

    if cmap == None:
        cmap = "Greys"
    cm = mpl.cm.get_cmap(cmap, 256)

    # New map based on cmap with 256 colors and alpha as specified
    newmap = cm(np.linspace(0, 1, 256))
    newmap[:, 3] = alpha

    if clim is None:
        epsmax = np.amax(eps_r)
        # Get the minimum value that's larger than the PEC value
        cmin = np.amin(eps_r[eps_r > pec_eps], initial=epsmax)
        cl = [cmin, epsmax + 256 * fp_eps]
    else:
        cl = list(clim)

    # Make sure we're larger than the PEC value
    # PMC and PEC colors are appended below
    cl[0] = max(cl[0], pec_eps)

    # Make eps = 1 completely transparent if it is at the lower bound
    if np.abs(cl[0] - 1) < fp_eps:
        newmap[0, 3] = 0

    bounds = np.hstack(
        (pmc_eps - 1, pec_eps - 1, np.linspace(cl[0], cl[1], 256))
    )
    eps_cmap = np.vstack(([0, 0, 1, 1], [1, 0, 0, 1], newmap))
    norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=258)

    return mpl.colors.ListedColormap(eps_cmap), norm, bounds


def _plot_eps(
    eps_r,
    cmap=None,
    clim=None,
    ax=None,
    extent=None,
    cbar=False,
    cax=None,
    alpha=1,
):

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)


    if len(eps_r.shape) < 2:
        log_and_raise(
            "Cross-section has less than two dimensions.", RuntimeError
        )

    cmplot, norm, bounds = _eps_cmap(eps_r, alpha, cmap, clim)

    im = ax.imshow(
        eps_r,
        interpolation="none",
        norm=norm,
        cmap=cmplot,
        origin="lower",
        extent=extent,
    )

    if cbar:
        if cax is not None:
            plt.colorbar(im, ax=ax, cax=cax, boundaries=bounds[2:])
        else:
            plt.colorbar(im, ax=ax, boundaries=bounds[2:])

    return im


def _mat_cmap(mat_inds, alpha=1, cmap=None):

    if cmap == None:
        # Define a custom colormap by picking colors not used for other stuff
        m0 = mpl.cm.get_cmap("tab20")(np.linspace(0, 1, 20))
        m1 = mpl.cm.get_cmap("tab20b")(np.linspace(0, 1, 20))
        m2 = mpl.cm.get_cmap("tab20c")(np.linspace(0, 1, 20))
        mc = np.vstack((m0, m1, m2))
        pick_c = [20, 32, 36, 28, 56, 22, 34, 38, 29, 58, 21, 33, 37, 10, 57]
        pick_c += [23, 35, 39, 11, 59]
        newmap = mc[pick_c, :]

        # ncl colors total, repeating if more materials present
        ncl = newmap.shape[0]
        newmap = np.tile(newmap, (200 // ncl + 1, 1))
        newmap = newmap[:200, :]
    else:
        cm = mpl.cm.get_cmap(cmap)
        # New map based on cmap for up to 200 materials
        newmap = cm(np.linspace(0, 1, 200))
        newmap[:, 3] = alpha

    bounds = np.hstack(
        (pmc_eps - 1, pec_eps - 1, -1.5, np.arange(0, 200) - 0.5)
    )
    mat_cmap = np.vstack(([0, 0, 1, 1], [1, 0, 0, 1], [0, 0, 0, 0], newmap))
    norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=203)

    return mpl.colors.ListedColormap(mat_cmap), norm, bounds, newmap


def _plot_mat(
    mat_inds,
    mat_names,
    cmap=None,
    ax=None,
    extent=None,
    legend=False,
    alpha=1,
):

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    if len(mat_inds.shape) < 2:
        log_and_raise(
            "Cross-section has less than two dimensions.", RuntimeError
        )

    cmplot, norm, bounds, newmap = _mat_cmap(mat_inds, alpha, cmap)
    im = ax.imshow(
        mat_inds,
        interpolation="none",
        norm=norm,
        cmap=cmplot,
        origin="lower",
        extent=extent,
    )

    if legend==True:
        labels = []
        for imat, mat in enumerate(mat_names):
            ax.plot(extent[1]+1, extent[3]+1, "s", color=newmap[imat, :])
            labels.append(mat)

        ax.legend(labels, borderaxespad=0., bbox_to_anchor=(1.02, 1))

    return im


def _get_inside(objects, coords):
    """Get a mask defining points inside a list of objects.

    Parameters
    ----------
    objects : list of Source or Monitor objects
    coords : tuple of 3 1D arrays

    Returns
    -------
    mask : np.ndarray
        Array indicating if the centers of the ``coords`` are inside any of the
        Sources or Monitors in the list.
    """

    Nx, Ny, Nz = [c.size - 1 for c in coords]

    mask = np.zeros((Nx, Ny, Nz))
    for obj in objects:
        mtmp = obj._inside(coords)
        mask[mtmp > 0] = 1

    return mask


def _plot_structures(
    sim,
    val="eps",
    normal="x",
    position=0.0,
    ax=None,
    cbar=False,
    clim=None,
    source_alpha=0.3,
    monitor_alpha=0.3,
    pml_alpha=0.2,
    frequency=None,
    legend=False,
):
    """Plot either the real part of the permittivity (val=='eps') or the
    material index of the structures (val=='mat')."""

    grid = sim.grid
    position = float(position)

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    # Get normal and cross-section axes indexes
    norm = xyz_dict[normal]
    cross = [0, 1, 2]
    cross.pop(norm)

    """ Get mesh for permittivity discretization.
    Use ``coords`` for the source/monitor plotting to ensure that 
    zero-size dimensions are taken to be in the same Yee cell as ``position``.
    We always break the symmetry such that if an object center is 
    sitting exactly on a coord, it will be taken to the right. """
    mesh = [[], [], []]
    coords = [[], [], []]
    cnorm = grid.coords[norm] - fp_eps
    ind = np.nonzero((position >= cnorm[:-1]) * (position < cnorm[1:]))[0]
    if ind.size == 0:
        log_and_raise(
            "Plane position outside of simulation domain.", RuntimeError
        )
    else:
        ind = ind[0]

    mesh[norm] = np.array([position])
    if np.abs(position) < fp_eps:
        mesh[norm] += 10*fp_eps
    mesh[cross[0]] = grid.mesh[cross[0]]
    mesh[cross[1]] = grid.mesh[cross[1]]

    coords[norm] = np.array([cnorm[ind], cnorm[ind+1]])
    coords[cross[0]] = grid.coords[cross[0]]
    coords[cross[1]] = grid.coords[cross[1]]

    # Set axes xlim and ylim if not provided
    sim_xlim = (grid.mesh[cross[0]][0], grid.mesh[cross[0]][-1])
    sim_ylim = (grid.mesh[cross[1]][0], grid.mesh[cross[1]][-1])

    # Define axes extent, labels and title
    extent = list(sim_xlim) + list(sim_ylim)
    x_lab = xyz_list[cross[0]]
    y_lab = xyz_list[cross[1]]
    ax_tit = x_lab + y_lab
    ax_tit += "-plane at " + xyz_list[norm] + "=%1.2eum" % position

    # Transparent color
    transp = (0, 0, 0, 0)
    # Colors for monitors, sources, pml, and border
    mnt_color = (236 / 255, 203 / 255, 32 / 255)
    src_color = (78 / 255, 145 / 255, 78 / 255)
    pml_color = (229 / 255, 127 / 255, 25 / 255)
    pbc_color = (75 / 255, 0, 130 / 255)

    # # Set axis background color
    # ax.set_facecolor(pml_color)

    # Plot and set axes properties
    if val == "eps":
        mat_disp = [mat.dispmod is not None for mat in sim.materials]
        if np.any(mat_disp) and frequency == None:
            logging.warning("Permittivity value of dispersive materials taken "
                "as epsilon_infty. Consider providing 'frequency' for "
                "the plotting, or using 'viz_mat_2D' instead.")
        eps_r = np.real(np.squeeze(sim._get_eps(mesh, freq=frequency))).T
        im = _plot_eps(eps_r, clim=clim, ax=ax, extent=extent, cbar=cbar)
    elif val == "mat":
        minds = np.squeeze(sim._get_mat(mesh)).T
        mnames = sim._mat_names
        im = _plot_mat(minds, mnames, ax=ax, extent=extent, legend=legend)

    ax.set_xlabel(x_lab + " (um)")
    ax.set_ylabel(y_lab + " (um)")
    ax.set_title(ax_tit)

    # Plot simulation domain borders depending on boundaries
    npml = sim.Npml[[cross[0], cross[1]], :]
    # In order of bottom, right, top, left
    border_pmls = [npml[1, 0], npml[0, 1], npml[1, 1], npml[0, 0]]
    x_border = [extent[0], extent[1], extent[1], extent[0], extent[0]]
    y_border = [extent[2], extent[2], extent[3], extent[3], extent[2]]
    for ib, bpml in enumerate(border_pmls):
        if bpml > 0:
            border_color = pml_color
        else:
            border_color = pbc_color
        ax.plot(
            [x_border[ib], x_border[ib + 1]],
            [y_border[ib], y_border[ib + 1]],
            color=border_color,
        )

    def squeeze_mask(mask, axis):
        inds = [slice(None), slice(None), slice(None)]
        inds[axis] = 0
        return np.squeeze(mask[tuple(inds)])

    if monitor_alpha > 0:
        mnt_alpha = min(monitor_alpha, 1)
        mnt_c = list(mnt_color)
        mnt_c.append(mnt_alpha)
        mnt_mask = squeeze_mask(_get_inside(sim.monitors, coords), norm)
        mnt_cmap = mpl.colors.ListedColormap(np.array([transp, mnt_c]))
        ax.imshow(
            mnt_mask.T,
            clim=(0, 1),
            cmap=mnt_cmap,
            origin="lower",
            extent=extent,
        )

    if source_alpha > 0:
        src_alpha = min(source_alpha, 1)
        src_c = list(src_color)
        src_c.append(src_alpha)
        src_mask = squeeze_mask(_get_inside(sim.sources, coords), norm)
        src_cmap = mpl.colors.ListedColormap(np.array([transp, src_c]))
        ax.imshow(
            src_mask.T,
            clim=(0, 1),
            cmap=src_cmap,
            origin="lower",
            extent=extent,
        )

    if pml_alpha > 0:
        pml_alpha = min(pml_alpha, 1)
        pml_c = list(pml_color)
        pml_c.append(pml_alpha)
        pml_mask = np.squeeze(np.zeros(tuple(m.size for m in mesh)))
        N1, N2 = pml_mask.shape
        pml_mask[: npml[0, 0], :] = 1
        pml_mask[N1 - npml[0, 1] :, :] = 1
        pml_mask[:, : npml[1, 0]] = 1
        pml_mask[:, N2 - npml[1, 1] :] = 1
        pml_cmap = mpl.colors.ListedColormap(np.array([transp, pml_c]))
        ax.imshow(
            pml_mask.T,
            clim=(0, 1),
            cmap=pml_cmap,
            origin="lower",
            extent=extent,
        )

    return im


def viz_eps_2D(
    self,
    normal="x",
    position=0.0,
    ax=None,
    cbar=False,
    clim=None,
    source_alpha=0.3,
    monitor_alpha=0.3,
    pml_alpha=0.2,
    frequency=None,
):
    """Plot the real part of the relative permittivity distribution of a
    2D cross-section of the simulation.

    Parameters
    ----------
    normal : {'x', 'y', 'z'}
        Axis normal to the cross-section plane.
    position : float, optional
        Position offset along the normal axis.
    ax : Matplotlib axis object, optional
        If ``None``, a new figure is created.
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    source_alpha : float, optional
        If larger than zero, overlay all sources in the simulation,
        with opacity defined by ``source_alpha``.
    monitor_alpha : float, optional
        If larger than zero, overlay all monitors in the simulation,
        with opacity defined by ``monitor_alpha``.
    pml_alpha : float, optional
        If larger than zero, overlay the PML boundaries of the simulation,
        with opacity defined by ``pml_alpha``.
    frequency : float or None, optional
        (Hz) frequency at which to query the permittivity. If
        ``None``, the instantaneous :math:`\\epsilon_\\infty` is used.

    Returns
    -------
    Matplotlib image object

    Note
    ----
    The plotting is discretized at the center positions of the Yee grid and
    is for illustrative purposes only. It does not exactly match the
    discretization used in the solver.
    """

    return _plot_structures(
        self,
        "eps",
        normal=normal,
        position=position,
        ax=ax,
        cbar=cbar,
        clim=clim,
        source_alpha=source_alpha,
        monitor_alpha=monitor_alpha,
        pml_alpha=pml_alpha,
        frequency=frequency,
    )


def viz_mat_2D(
    self,
    normal="x",
    position=0.0,
    ax=None,
    source_alpha=0.3,
    monitor_alpha=0.3,
    pml_alpha=0.2,
    legend=False
):
    """Visualize the structures in a 2D cross-section of the simulation
    using a fake-color coding based on material index in the list of materials.
    
    Parameters
    ----------
    normal : {'x', 'y', 'z'}
        Axis normal to the cross-section plane.
    position : float, optional
        Position offset along the normal axis.
    ax : Matplotlib axis object, optional
        If ``None``, a new figure is created.
    source_alpha : float, optional
        If larger than zero, overlay all sources in the simulation,
        with opacity defined by ``source_alpha``.
    monitor_alpha : float, optional
        If larger than zero, overlay all monitors in the simulation,
        with opacity defined by ``monitor_alpha``.
    pml_alpha : float, optional
        If larger than zero, overlay the PML boundaries of the simulation,
        with opacity defined by ``pml_alpha``.
    legend : bool, optional
        If ``True``, a legend with the material names is shown.
    
    Note
    ----
    The plotting is discretized at the center positions of the Yee grid and
    is for illustrative purposes only. It does not exactly match the
    discretization used in the solver.
    
    No Longer Returned
    ------------------
    Matplotlib image object
    """

    return _plot_structures(
        self,
        "mat",
        normal=normal,
        position=position,
        ax=ax,
        source_alpha=source_alpha,
        monitor_alpha=monitor_alpha,
        pml_alpha=pml_alpha,
        legend=legend
    )


def _structure_png(self, folder_path, val="mat", aspect_ratio=None):
    """
    Export png images of 2D cross-sections of the simulation at the domain
    center in x, y, and z.

    Parameters
    ----------
    folder_path : string
        Path in which the images will be exported.
    val : str, optional
        'eps' or 'mat', whether to plot based on permittivity or material.
    aspect_ratio : float or None
        Fix the width/height image ratio. If ``None``, the smallest aspect
        ratio of the three plots is used in all.
    """

    figs = [
        plt.figure(0, constrained_layout=True),
        plt.figure(1, constrained_layout=True),
        plt.figure(2, constrained_layout=True),
    ]
    ims = []
    clims = []
    norm_ims = [] # stores the indexes for successfully plotted images

    if not aspect_ratio:
        # Take the smallest aspect ratio
        sim_ars = [
            self.size[1] / self.size[2],
            self.size[0] / self.size[2],
            self.size[0] / self.size[1],
        ]
        aspect_ratio = np.min(sim_ars)

    for norm_ind, normal in enumerate(["x", "y", "z"]):
        cinds = [0, 1, 2]
        cinds.pop(norm_ind)
        ax = figs[norm_ind].add_subplot(111)
        sim_width = self.size[cinds[0]]
        sim_height = self.size[cinds[1]]
        sim_aspect = sim_width / sim_height
        if sim_aspect > aspect_ratio:
            new_height = sim_width / aspect_ratio
            ax.set_ylim(-new_height / 2, new_height / 2)
        elif sim_aspect < aspect_ratio:
            new_width = sim_height * aspect_ratio
            ax.set_xlim(-new_width / 2, new_width / 2)
        try:
            if val == "eps":
                im = self.viz_eps_2D(normal, self.center[norm_ind], ax)
                eps_r = np.array(im.get_array())
                epsmax = np.amax(eps_r)
                epsmin = np.amin(eps_r[eps_r > pec_eps], initial=epsmax)
                clims.append([epsmin, epsmax])
            elif val == "mat":
                im = self.viz_mat_2D(normal, self.center[norm_ind], ax)
            ims.append(im)
            norm_ims.append(norm_ind)
        except:
            logging.warning(f"Could not export image for normal {normal}!")

    print(figs, ims, norm_ims)

    if val == "eps":
        # Set the same clims in all plots
        clims = np.array(clims)
        clim_glob = [np.amin(clims[:, 0]), np.amax(clims[:, 1])]
        # Get a new color norm based on the global clims. eps_r is irrelevant.
        _, norm, _ = _eps_cmap(eps_r, clim=clim_glob)

    # Set new clims and save figures
    for norm_ind, normal in enumerate(["x", "y", "z"]):
        fname = "simulation_%scent.png" % normal
        plt.figure(norm_ind)
        if norm_ind in norm_ims:
            # if val == "eps":
            #     ims[norm_ims.index(norm_ind)].set_norm(norm)
            plt.savefig(folder_path + fname, dpi=150)
        plt.close(figs[norm_ind])
