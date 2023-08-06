# -*- coding: utf-8 -*-


def set_m(self, value):
    """Convert the value the correct m unit (to set in the object in m)

    Parameters
    ----------
    self : Unit
        A Unit object
    value : float
        Value to convert

    Returns
    -------
    value: float
        value converted in [m]
    """
    if self.unit_m == 1:  # Convert to mm
        return value / 1000
    else:
        return value
