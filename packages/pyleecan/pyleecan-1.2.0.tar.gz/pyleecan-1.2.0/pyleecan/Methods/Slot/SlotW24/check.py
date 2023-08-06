# -*- coding: utf-8 -*-

from numpy import arcsin, pi

from ....Methods.Slot.Slot import SlotCheckError
from ....Methods.Slot.SlotW24 import *


def check(self):
    """Check that the SlotW24 object is correct

    Parameters
    ----------
    self : SlotW24
        A SlotW24 object

    Returns
    -------
    None

    Raises
    -------
    S24_W3CheckError
        The teeth are too wide, reduce Zs or W3
    S24_HWCheckError
        The teeth are too wide, reduce Zs, H2 or W3
    """
    Rbo = self.get_Rbo()

    if 2 * arcsin(self.W3 / (2 * Rbo)) > 2 * pi / self.Zs:
        raise S24_W3CheckError("The teeth are too wide, reduce Zs or W3")

    if (
        not self.is_outwards()
        and 2 * arcsin(self.W3 / (2 * Rbo - self.H2)) > 2 * pi / self.Zs
    ):
        raise S24_HWCheckError("The teeth are too wide, reduce Zs, H2 or W3")
