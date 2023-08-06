# -*- coding: utf-8 -*-
from numpy import pi

from ....Classes.LamSlot import LamSlot


def build_geometry(self, is_magnet=True, sym=1, alpha=0, delta=0, is_simplified=False):
    """Build the geometry of the LamSlotMag

    Parameters
    ----------
    self : LamSlotMag
        LamSlotMag object
    is_magnet : bool
        If True build the magnet surfaces
    sym : int
        Symmetry factor (1= full machine, 2= half of the machine...)
    alpha : float
        Angle for rotation [rad]
    delta : complex
        Complex value for translation
    is_simplified: bool
        True to avoid line superposition

    Returns
    -------
    surf_list : list
        list of surfaces needed to draw the lamination

    """

    if self.is_stator:
        st = "Stator"
    else:
        st = "Rotor"

    assert (self.slot.Zs % sym) == 0, (
        "ERROR, Wrong symmetry for "
        + st
        + " "
        + str(self.slot.Zs)
        + " slots and sym="
        + str(sym)
    )
    # getting the LamSlot surface
    surf_list = LamSlot.build_geometry(self, sym=sym)

    Zs = self.slot.Zs
    slot_pitch = 2 * pi / Zs

    # Add the magnet surface(s)
    if is_magnet and self.magnet is not None:
        # for each magnet to draw
        for ii in range(Zs // sym):
            mag_surf = self.slot.get_surface_active(
                alpha=slot_pitch * ii + slot_pitch * 0.5
            )
            # Defining type of magnetization of the magnet
            if self.magnet.type_magnetization == 0:
                type_mag = "Radial"
            elif self.magnet.type_magnetization == 1:
                type_mag = "Parallel"
            elif self.magnet.type_magnetization == 2:
                type_mag = "Hallbach"
            else:
                type_mag = ""

            surf_list.append(mag_surf)
            # Adapt the label
            if ii % 2 != 0:  # South pole
                surf_list[-1].label = (
                    "Magnet" + st + type_mag + "_S_R0" + "_T0_S" + str(ii)
                )
            else:  # North pole
                surf_list[-1].label = (
                    "Magnet" + st + type_mag + "_N_R0" + "_T0_S" + str(ii)
                )

    # Apply the transformations
    for surf in surf_list:
        surf.rotate(alpha)
        surf.translate(delta)

    return surf_list
