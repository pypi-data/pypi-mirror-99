# -*- coding: utf-8 -*-

from numpy import cos


def comp_height(self):
    """Compute the height of the Slot.
    Caution, the bottom of the Slot is an Arc

    Parameters
    ----------
    self : SlotM15
        A SlotM15 object

    Returns
    -------
    Htot: float
        Height of the slot [m]

    """

    return self.H0
