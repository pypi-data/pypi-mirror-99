# -*- coding: utf-8 -*-

from numpy import pi
from ....Classes.Lamination import Lamination


def comp_volumes(self):
    """Compute the Lamination volumes

    Parameters
    ----------
    self : LamHole
        A LamHole object

    Returns
    -------
    V_dict: dict
        Lamination volume dictionnary (Vlam, Vvent, Vmag, Vhole) [m**3]

    """

    V_dict = Lamination.comp_volumes(self)
    Lt = self.comp_length()

    Vhole = 0
    Vmag = 0
    for hole in self.hole:
        Vhole += hole.Zh * hole.comp_surface() * Lt
        if hole.has_magnet():
            Vmag += hole.Zh * hole.comp_volume_magnets()

    V_dict["Vmag"] = Vmag
    V_dict["Vhole"] = Vhole

    return V_dict
