# -*- coding: utf-8 -*-

from ....Classes.Lamination import Lamination
from ....Methods.Machine.LamSlotWind import *


def check(self):
    """Check that the Lamination object is correct

    Parameters
    ----------
    self :
        A LamSlotWind object

    Returns
    -------
    None

    Raises
    _______
    LWC_SlotTooLong
        The Slot is too long for the lamination (HYoke <0)
    LWC_MismatchPhase
        The Winding and the Converter don't have the same number of phase
    LWC_OverlappingSlot
        The Lamination has overlapping slot
    """

    Lamination.check(self)

    self.winding.conductor.check()
    self.slot.check()

    if self.comp_height_yoke() < 0:
        raise LWC_SlotTooLong("The Slot is too long for the lamination " "(HYoke <0)")

    """
    Wt = self.slot.comp_tooth_widths()["WTooth_min"]

    if Wt < 0:
        raise LWC_OverlappingSlot("The Lamination has overlapping slot")
    """
