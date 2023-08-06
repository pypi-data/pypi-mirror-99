# -*- coding: utf-8 -*-

from matplotlib.patches import Patch, Polygon
from matplotlib.pyplot import axis, legend
from numpy import array, exp, pi

from ....definitions import config_dict
from ....Functions.init_fig import init_fig
from ....Functions.Winding.gen_phase_list import gen_name

PHASE_COLORS = config_dict["PLOT"]["COLOR_DICT"]["PHASE_COLORS"]


def plot_active(
    self,
    wind_mat=None,
    fig=None,
    is_bar=False,
    is_show_fig=True,
    enforced_default_color=None,
    alpha=0,
    delta=0,
):
    """Plot the active area of the lamination according to the wind_mat

    Parameters
    ----------
    self : Slot
        A Slot object
    wind_mat : numpy.ndarray
        A matrix [Nrad,Ntan,Zs,qs] representing the active (Default value = None)
    fig :
        if None, open a new fig and plot, else add to the current
        one (Default value = None)
    is_bar : bool
        To adapt the legend text for squirrel cage bar (Default value = False)
    is_show_fig : bool
        To call show at the end of the method
    enforced_default_color : str
        If not None enforce the active color (when wind_mat is None)
    alpha : float
        Angle for rotation (Default value = 0) [rad]
    delta : Complex
        complex for translation (Default value = 0)
    Returns
    -------
    None
    """

    if enforced_default_color is None:
        enforced_default_color = PHASE_COLORS[0]

    if wind_mat is None:  # Default : Only one zone monocolor
        Nrad, Ntan, qs = 1, 1, 1
        Zs = self.Zs
    else:
        (Nrad, Ntan, Zs, qs) = wind_mat.shape
    qs_name = gen_name(qs)

    surf_list = self.build_geometry_active(Nrad, Ntan, alpha=alpha, delta=delta)

    patches = list()
    for ii in range(len(surf_list)):
        # Compute the coordinate for one zone
        point_list = list()
        for curve in surf_list[ii].get_lines():
            point_list.extend(curve.discretize().tolist())
        point_list = array(point_list)

        for jj in range(Zs):
            if wind_mat is None or len(surf_list) != Ntan * Nrad:
                x, y = point_list.real, point_list.imag
                patches.append(Polygon(list(zip(x, y)), color=enforced_default_color))
            else:
                # print "Nrad, Ntan, Zs : "+str((ii%Nrad,ii/Nrad,jj))
                color = get_color(wind_mat, ii % Nrad, ii // Nrad, jj)
                x, y = point_list.real, point_list.imag
                patches.append(Polygon(list(zip(x, y)), color=color))
            point_list = point_list * exp(1j * (2 * pi) / self.Zs)

    # Display the result
    (fig, axes, patch_leg, label_leg) = init_fig(fig)
    axes.set_xlabel("(m)")
    axes.set_ylabel("(m)")
    axes.set_title("Winding Pattern")

    # Add the magnet to the fig
    for patch in patches:
        axes.add_patch(patch)

    # Axis Setup
    axis("equal")
    Rbo = self.get_Rbo()

    Lim = Rbo * 1.2
    axes.set_xlim(-Lim, Lim)
    axes.set_ylim(-Lim, Lim)

    # Legend setup
    if wind_mat is None or len(surf_list) != Ntan * Nrad:
        # No winding matrix => Only one zone
        if not is_bar and not ("Winding" in label_leg):
            # Avoid adding twice the same label
            patch_leg.append(Patch(color=PHASE_COLORS[0]))
            label_leg.append("Winding")
        elif is_bar and not ("Rotor bar" in label_leg):
            # Avoid adding twice the same label
            patch_leg.append(Patch(color=PHASE_COLORS[0]))
            label_leg.append("Rotor bar")
    else:  # Add every phase to the legend
        for ii in range(qs):
            if not ("Phase " + qs_name[ii] in label_leg):
                # Avoid adding twice the same label
                index = ii % len(PHASE_COLORS)
                patch_leg.append(Patch(color=PHASE_COLORS[index]))
                label_leg.append("Phase " + qs_name[ii])

    legend(patch_leg, label_leg)
    if is_show_fig:
        fig.show()


def get_color(wind_mat, Nrad, Ntan, Zs):
    """Return the color (corresponding phase) for the zone (Nrad,Ntan,Zs)

    Parameters
    ----------
    wind_mat :
        A matrix [Nrad,Ntan,Zs,qs] representing the winding
    Nrad :
        Zone radial coordinate
    Ntan :
        Zone tagential coordinate
    Zs :
        Zone slot number coordinate

    Returns
    -------
    str
        color: Color of the zone

    """
    A = wind_mat[Nrad, Ntan, Zs, :]
    for zz in range(len(A)):
        if A[zz] != 0:
            return PHASE_COLORS[zz]
    return "w"  # If all the phase are at 0 : the zone is empty => white
