# -*- coding: utf-8 -*-
from numpy import pi, exp, arcsin


def _comp_point_coordinate(self):
    """Compute the point coordinate needed to plot the Slot.

    Parameters
    ----------
    self : SlotW61
        A SlotW61 object

    Returns
    -------
    point_list: list
        A list of 11 complex

    """

    Rbo = self.get_Rbo()
    hsp = pi / self.Zs
    alpha = float(arcsin(self.W0 / (2 * Rbo)))

    # Zxt => In the tooth ref (Ox as the sym axis of the tooth)
    Z1t = Rbo * exp(1j * alpha)
    Z2t = Z1t.real - self.H0 + 1j * self.W1 / 2
    Z3t = Z2t - self.H1
    Z4t = Z3t - 1j * (self.W1 - self.W2) / 2
    Z5t = Z4t - self.H2

    # Go to the slot ref
    Z1 = Z1t * exp(-1j * hsp)
    Z2 = Z2t * exp(-1j * hsp)
    Z3 = Z3t * exp(-1j * hsp)
    Z4 = Z4t * exp(-1j * hsp)
    Z5 = Z5t * exp(-1j * hsp)
    Z6 = Z5.conjugate()
    Z7 = Z4.conjugate()
    Z8 = Z3.conjugate()
    Z9 = Z2.conjugate()
    Z10 = Z1.conjugate()

    return [Z1, Z2, Z3, Z4, Z5, Z6, Z7, Z8, Z9, Z10]
