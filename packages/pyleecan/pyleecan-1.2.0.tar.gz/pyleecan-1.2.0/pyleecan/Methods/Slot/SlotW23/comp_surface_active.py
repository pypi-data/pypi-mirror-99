# -*- coding: utf-8 -*-

from numpy import arcsin, sin, sqrt


def comp_surface_active(self):
    """Compute the Slot inner surface for winding (by analytical computation)

    Parameters
    ----------
    self : SlotW21
        A SlotW21 object

    Returns
    -------
    Swind: float
        Slot inner surface for winding [m**2]

    """

    Rbo = self.get_Rbo()

    # By Pythagore
    # self.H2 projection
    H2 = sqrt(self.H2 ** 2 - ((self.W2 - self.W1) / 2.0) ** 2)
    S2 = 0.5 * (self.W1 + self.W2) * H2

    if self.is_outwards():
        Rslot = Rbo + self.comp_height()  # External radius of the slot
        alpha = float(2 * arcsin(self.W2 / (2 * Rslot)))  # W2 in rad
        S3 = (Rslot ** 2.0) / 2.0 * (alpha - sin(alpha))
        return S2 + S3
    else:
        Rslot = Rbo - self.comp_height()  # External radius of the slot
        alpha = float(2 * arcsin(self.W2 / (2 * Rslot)))  # W2 in rad
        S3 = (Rslot ** 2.0) / 2.0 * (alpha - sin(alpha))
        return S2 - S3
