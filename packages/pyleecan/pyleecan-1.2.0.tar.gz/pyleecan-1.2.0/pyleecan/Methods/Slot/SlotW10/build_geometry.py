# -*- coding: utf-8 -*-
from ....Classes.Segment import Segment


def build_geometry(self):
    """Compute the curve (Line) needed to plot the Slot.
    The ending point of a curve is the starting point of the next curve in
    the list

    Parameters
    ----------
    self : SlotW10
        A SlotW10 object

    Returns
    -------
    curve_list: list
        A list of 10 Segments

    """
    point_dict = self._comp_point_coordinate()
    Z1 = point_dict["Z1"]
    Z2 = point_dict["Z2"]
    Z3 = point_dict["Z3"]
    Z4 = point_dict["Z4"]
    Z5 = point_dict["Z5"]
    Z6 = point_dict["Z6"]
    Z7 = point_dict["Z7"]
    Z8 = point_dict["Z8"]
    Z9 = point_dict["Z9"]
    Z10 = point_dict["Z10"]

    # Creation of curve
    curve_list = list()
    if self.H0 > 0:
        curve_list.append(Segment(Z1, Z2))
    if self.H1 > 0 and self.W1 > self.W0:
        curve_list.append(Segment(Z2, Z3))
    if self.W1 > self.W0:
        curve_list.append(Segment(Z3, Z4))
    curve_list.append(Segment(Z4, Z5))
    if self.W2 > 0:
        curve_list.append(Segment(Z5, Z6))
    curve_list.append(Segment(Z6, Z7))
    if self.W1 > self.W0:
        curve_list.append(Segment(Z7, Z8))
    if self.H1 > 0 and self.W1 > self.W0:
        curve_list.append(Segment(Z8, Z9))
    if self.H0 > 0:
        curve_list.append(Segment(Z9, Z10))

    return curve_list
