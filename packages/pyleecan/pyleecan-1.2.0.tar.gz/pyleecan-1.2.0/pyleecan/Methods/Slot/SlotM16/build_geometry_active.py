# -*- coding: utf-8 -*-

from numpy import zeros, linspace
from ....Classes.Segment import Segment
from ....Classes.SurfLine import SurfLine


def build_geometry_active(self, Nrad, Ntan, is_simplified=False, alpha=0, delta=0):
    """Split the slot winding area in several zone

    Parameters
    ----------
    self : SlotM16
        A SlotM16 object
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
    surf_list: list
        List of surface delimiting the winding zone

    """

    # get the name of the lamination
    st = self.get_name_lam()

    [Z12, Z11, Z10, Z9, Z8, Z7, Z6, Z5, Z4, Z3, Z2, Z1] = self._comp_point_coordinate()

    X = linspace(Z8, Z7, Nrad + 1)

    # Nrad+1 and Ntan+1 because 3 points => 2 zones
    Z = zeros((Nrad + 1, Ntan + 1), dtype=complex)
    for ii in range(Nrad + 1):
        Z[ii][:] = linspace(X[ii], X[ii].conjugate(), Ntan + 1)

    assert Z[0][0] == Z8
    assert Z[Nrad][0] == Z7
    assert Z[0][Ntan] == Z5
    assert Z[Nrad][Ntan] == Z6
    Z_8 = Z5 + (self.W2 / 2) + (self.W1 / 2)
    Z_5 = Z5 + (self.W2 / 2) - (self.W1 / 2)
    # We go thought the zone by Rad then Tan, starting by (0,0)
    surf_list = list()
    for jj in range(Ntan):  # jj from 0 to Ntan-1
        for ii in range(Nrad):  # ii from 0 to Nrad-1
            Z1 = Z[ii][jj]
            Z2 = Z[ii][jj + 1]
            Z3 = Z[ii + 1][jj + 1]
            Z4 = Z[ii + 1][jj]
            point_ref = (Z1 + Z2 + Z3 + Z4) / 4
            # With one zone the order would be [Z7,Z4,Z5,Z6]
            if is_simplified:
                curve_list = list()
                if ii == 0:
                    if Z1 > Z_8 and Z_5 < Z2 < Z_8:
                        curve_list.append(Segment(Z_8, Z2))
                    elif Z_5 < Z1 < Z_8 and Z_5 < Z2 < Z_8:
                        curve_list.append(Segment(Z1, Z2))
                    elif Z2 < Z_5 and Z_5 < Z1 < Z_8:
                        curve_list.append(Segment(Z1, Z_5))

                if jj != Ntan - 1:
                    curve_list.append(Segment(Z2, Z3))
                if ii != Nrad - 1:
                    curve_list.append(Segment(Z3, Z4))
                label = "Wind_" + st + "_R" + str(ii) + "_T" + str(jj) + "_S0"
                surface = SurfLine(
                    line_list=curve_list, label=label, point_ref=point_ref
                )
                surf_list.append(surface)
            else:
                curve_list = list()
                curve_list.append(Segment(Z1, Z2))
                curve_list.append(Segment(Z2, Z3))
                curve_list.append(Segment(Z3, Z4))
                curve_list.append(Segment(Z4, Z1))
                surface = SurfLine(
                    line_list=curve_list,
                    label="Wind_" + st + "_R" + str(ii) + "_T" + str(jj) + "_S0",
                    point_ref=point_ref,
                )
                surf_list.append(surface)

    for surf in surf_list:
        surf.rotate(alpha)
        surf.translate(delta)
    return surf_list
