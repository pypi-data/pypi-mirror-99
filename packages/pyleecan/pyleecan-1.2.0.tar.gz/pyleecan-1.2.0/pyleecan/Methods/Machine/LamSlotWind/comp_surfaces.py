# -*- coding: utf-8 -*-

from numpy import pi
from ....Classes.LamSlot import LamSlot


def comp_surfaces(self):
    """Compute the Lamination surfaces (Slam, Svent, Sslot, Swind)

    Parameters
    ----------
    self : LamSlotWind
        A LamSlotWind object

    Returns
    -------
    S_dict: dict
        Lamination surface dictionnary (Slam, Svent, Sslot, Swind) [m**2]

    """

    S_dict = LamSlot.comp_surfaces(self)

    if self.slot is not None:
        S_dict["Swind"] = self.get_Zs() * self.slot.comp_surface_active()
    else:
        S_dict["Swind"] = 0

    return S_dict
