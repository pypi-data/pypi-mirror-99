# -*- coding: utf-8 -*-
from numpy import angle as np_angle, exp, linspace

from ....Methods.Machine import ARC_NPOINT_D
from ....Methods.Geometry.Arc2 import NbPointArc2DError


def discretize(self, nb_point=ARC_NPOINT_D):
    """Return the discretize version of the Arc.
    Begin and end are always returned

    Parameters
    ----------
    self : Arc2
        An Arc2 object
    nb_point : int
        Number of points to add to discretize the arc (Default value = ARC_NPOINT_D)

    Returns
    -------
    list_point: list
        list of complex coordinate of the points

    Raises
    ------
    NbPointArc2DError
        nb_point must be an integer >=0
    """

    self.check()
    if not isinstance(nb_point, int):
        raise NbPointArc2DError("discretize : nb_point must be an integer")
    if nb_point < 0:
        raise NbPointArc2DError("nb_point must be >=0")

    # We use the complex representation of the point
    z1 = self.begin
    zc = self.center

    # Geometric transformation : center is the origine, angle(begin) = 0
    Zstart = (z1 - zc) * exp(-1j * np_angle(z1 - zc))

    # Generation of the point by rotation
    t = linspace(0, self.angle, nb_point + 2)
    list_point = Zstart * exp(1j * t)

    # Geometric transformation : return to the main axis
    list_point = list_point * exp(1j * np_angle(z1 - zc)) + zc

    return list_point
