# -*- coding: utf-8 -*-

from numpy import angle, linspace
from scipy.optimize import fsolve

from ....Classes.Segment import Segment
from ....Classes.SurfLine import SurfLine
import matplotlib.pyplot as plt


def build_geometry_active(self, Nrad, Ntan, is_simplified=False, alpha=0, delta=0):
    """Split the slot active area in several zone
    This method assume that the active area is centered on X axis and symetrical
    Otherwise a dedicated build_geometry_active method must be provided

    Parameters
    ----------
    self : Slot
        A Slot object
    Nrad : int
        Number of radial layer
    Ntan : int
        Number of tangentiel layer
    is_simplified : bool
        boolean to specify if coincident lines are considered as one or different lines (Default value = False)
    alpha : float
        Angle for rotation (Default value = 0) [rad]
    delta : Complex
        complex for translation (Default value = 0)

    Returns
    -------
    surf_list:
        List of surface delimiting the active zone

    """

    assert Ntan in [1, 2]

    surf_act = self.get_surface_active()

    # Find the two intersection point with Ox axis
    inter_list = list()
    for line in surf_act.get_lines():
        inter_list.extend(line.intersect_line(0, 100))
    # When the two lines at the bottom cross on X axis (ex SlotW14)
    if len(inter_list) == 3 and abs(inter_list[0] - inter_list[1]) < 1e-6:
        inter_list.pop(0)
    assert len(inter_list) == 2

    if abs(inter_list[0]) < abs(inter_list[1]) and self.is_outwards():
        Ztan1 = inter_list[0]
        Ztan2 = inter_list[1]
    elif abs(inter_list[0]) > abs(inter_list[1]) and self.is_outwards():
        Ztan1 = inter_list[1]
        Ztan2 = inter_list[0]
    elif abs(inter_list[0]) < abs(inter_list[1]) and not self.is_outwards():
        Ztan1 = inter_list[1]
        Ztan2 = inter_list[0]
    elif abs(inter_list[0]) > abs(inter_list[1]) and not self.is_outwards():
        Ztan1 = inter_list[0]
        Ztan2 = inter_list[1]

    # First Tan split
    tan_list = list()
    if Ntan == 2:
        tan_list.append(
            surf_act.split_line(0, 100, is_top=False, is_join=True, label_join="")
        )
        tan_list.append(
            surf_act.split_line(0, 100, is_top=True, is_join=True, label_join="")
        )
    else:
        tan_list = [surf_act]

    # Rad split
    surf_list = list()
    X_list = linspace(Ztan1, Ztan2, Nrad + 1, True).tolist()[1:-1]
    for ii in range(Ntan):
        surf = tan_list[ii]
        if Nrad > 1:
            direct = self.is_outwards()
            for jj in range(Nrad - 1):
                X = X_list[jj]
                surf_list.append(
                    surf.split_line(
                        X - 100j, X + 100j, is_top=direct, is_join=True, label_join=""
                    )
                )
                surf = surf.split_line(
                    X - 100j, X + 100j, is_top=not direct, is_join=True, label_join=""
                )
            # Add the last surface
            surf_list.append(surf)
        else:  # add the radial surfaces without any other cut
            surf_list.append(surf.copy())

    # Set all label
    set_label(surf_list, Nrad, Ntan, self.get_name_lam())

    # Apply transformation
    for surf in surf_list:
        surf.rotate(alpha)
        surf.translate(delta)

    return surf_list


def set_label(surf_list, Nrad, Ntan, st):
    """Set the normalized label"""

    index = 0
    for jj in range(Ntan):
        for ii in range(Nrad):
            surf_list[index].label = (
                "Wind_" + st + "_R" + str(ii) + "_T" + str(jj) + "_S0"
            )
            index += 1
