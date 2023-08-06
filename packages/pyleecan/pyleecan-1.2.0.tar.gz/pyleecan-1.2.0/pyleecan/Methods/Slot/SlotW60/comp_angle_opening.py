# -*- coding: utf-8 -*-

from numpy import pi


def comp_angle_opening(self):
    """Compute the average opening angle of the Slot

    Parameters
    ----------
    self : SlotW60
        A SlotW60 object

    Returns
    -------
    alpha: float
        Average opening angle of the slot [rad]

    """

    return 2 * pi / self.Zs
