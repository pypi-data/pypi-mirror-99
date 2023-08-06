# -*- coding: utf-8 -*-

from matplotlib.patches import Patch, Rectangle
from matplotlib.pyplot import axis, legend, subplots
from ....definitions import config_dict

COND_COLOR = config_dict["PLOT"]["COLOR_DICT"]["PHASE_COLORS"][0].copy()
INS_COLOR = config_dict["PLOT"]["COLOR_DICT"]["PHASE_COLORS"][1].copy()
# Remove alpha from phases
COND_COLOR[3] = 1
INS_COLOR[3] = 1


def plot(self, is_show_fig=True):
    """Plot a Conductor in a matplotlib fig

    Parameters
    ----------
    self : CondType11
        A CondType11 object
    is_show_fig : bool
        To call show at the end of the method

    Returns
    -------
    None
    """

    patches_list = []

    # Conductor insulation
    Wcond = self.comp_width()
    Hcond = self.comp_height()
    patches_list.append(Rectangle((0, 0), Wcond, Hcond, color=INS_COLOR))

    # Wire conductor
    for ii in range(self.Nwppc_tan):
        for jj in range(self.Nwppc_rad):
            # Computation of bottom left corner coodinates
            x = self.Wins_wire + ii * (self.Wwire + 2 * self.Wins_wire)
            y = self.Wins_wire + jj * (self.Hwire + 2 * self.Wins_wire)
            patches_list.append(
                Rectangle((x, y), self.Wwire, self.Hwire, color=COND_COLOR)
            )

    # Display
    fig, ax = subplots()
    for patch in patches_list:
        ax.add_patch(patch)

    # Axis Setup
    axis("equal")

    # The conductor is centered
    ax.set_xlim(0 - Wcond / 10, Wcond * 11.0 / 10.0)
    ax.set_ylim(0 - Hcond / 10, Hcond * 11.0 / 10.0)

    # Legend
    patch_leg = list()  # Symbol
    label_leg = list()  # Text
    if self.Wins_wire > 0:
        patch_leg.append(Patch(color=INS_COLOR))
        label_leg.append("Wire insulation")

    patch_leg.append(Patch(color=COND_COLOR))
    label_leg.append("Active wire section")

    legend(patch_leg, label_leg)
    if is_show_fig:
        fig.show()
