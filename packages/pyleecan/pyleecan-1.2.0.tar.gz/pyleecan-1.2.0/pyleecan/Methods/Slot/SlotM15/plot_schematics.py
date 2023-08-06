import matplotlib.pyplot as plt
from numpy import pi, exp

from ....Classes.Arc1 import Arc1
from ....Classes.LamSlot import LamSlot
from ....Classes.Segment import Segment
from ....definitions import config_dict
from ....Functions.Plot import (
    ARROW_COLOR,
    ARROW_WIDTH,
    MAIN_LINE_COLOR,
    MAIN_LINE_STYLE,
    MAIN_LINE_WIDTH,
    P_FONT_SIZE,
    SC_FONT_SIZE,
    SC_LINE_COLOR,
    SC_LINE_STYLE,
    SC_LINE_WIDTH,
    TEXT_BOX,
    plot_quote,
)
from ....Methods import ParentMissingError

MAGNET_COLOR = config_dict["PLOT"]["COLOR_DICT"]["MAGNET_COLOR"]


def plot_schematics(
    self,
    is_default=False,
    is_add_point_label=False,
    is_add_schematics=True,
    is_add_main_line=True,
    type_add_active=True,
    save_path=None,
    is_show_fig=True,
):
    """Plot the schematics of the slot

    Parameters
    ----------
    self : SlotM15
        A SlotM15 object
    is_default : bool
        True: plot default schematics, else use current slot values
    is_add_point_label : bool
        True to display the name of the points (Z1, Z2....)
    is_add_schematics : bool
        True to display the schematics information (W0, H0...)
    is_add_main_line : bool
        True to display "main lines" (slot opening and 0x axis)
    type_add_active : int
        0: No active surface, 1: active surface as winding, 2: active surface as magnet
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    is_show_fig : bool
        To call show at the end of the method
    """

    # Use some default parameter
    if is_default:
        slot = type(self)(
            Zs=2, W0=60 * pi / 180, H0=0.03, Hmag=0.02, Wmag=0.05, Rtopm=0.05
        )
        lam = LamSlot(
            Rint=40e-3, Rext=0.11, is_internal=True, is_stator=False, slot=slot
        )

        slot.plot_schematics(
            is_default=False,
            is_add_point_label=is_add_point_label,
            is_add_schematics=is_add_schematics,
            is_add_main_line=is_add_main_line,
            type_add_active=type_add_active,
            save_path=save_path,
            is_show_fig=is_show_fig,
        )
    else:
        # Getting the main plot
        if self.parent is None:
            raise ParentMissingError("Error: The slot is not inside a Lamination")
        lam = self.parent
        lam.plot(alpha=pi / self.Zs, is_show_fig=False)  # center slot on Ox axis
        fig = plt.gcf()
        ax = plt.gca()
        point_dict = self._comp_point_coordinate()
        if self.is_outwards():
            sign = +1
        else:
            sign = -1
        Rbo = self.get_Rbo()

        # Adding point label
        if is_add_point_label:
            for name, Z in point_dict.items():
                ax.text(
                    Z.real,
                    Z.imag,
                    name,
                    fontsize=P_FONT_SIZE,
                    bbox=TEXT_BOX,
                )

        # Adding schematics
        if is_add_schematics:
            # W0
            R = Rbo + sign * self.H0 * 1.1
            line = Arc1(
                begin=R * exp(-1j * self.W0 / 2),
                end=R * exp(1j * self.W0 / 2),
                radius=R,
                is_trigo_direction=True,
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="W0",
                offset_label=point_dict["Z3"] - line.get_middle(),
                fontsize=SC_FONT_SIZE,
            )
            # Wmag
            plot_quote(
                Z1=point_dict["ZM2"],
                Zlim1=point_dict["ZM2"] - sign * self.Hmag,
                Zlim2=point_dict["ZM3"] - sign * self.Hmag,
                Z2=point_dict["ZM3"],
                offset_label=0.25 * self.Hmag,
                fig=fig,
                ax=ax,
                label="Wmag",
            )
            # H0
            line = Segment(point_dict["Z1"], point_dict["Z2"])
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="H0",
                offset_label=-1j * point_dict["Z4"].imag * 0.3,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # Hmag
            plot_quote(
                Z1=point_dict["ZM0"],
                Zlim1=point_dict["ZM0"] - 1j * 0.5 * self.Wmag,
                Zlim2=point_dict["ZM0"] + sign * self.Hmag - 1j * 0.5 * self.Wmag,
                Z2=point_dict["ZM0"] + sign * self.Hmag,
                offset_label=-1j * 0.2 * self.Wmag,
                fig=fig,
                ax=ax,
                label="Hmag",
            )
            # Rtopm
            line = Segment(point_dict["Zc"], point_dict["ZM0"])
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="Rtopm",
                offset_label=sign * self.Rtopm * 0.4
                + 1j * point_dict["ZM4"].imag * 0.3,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )

        if is_add_main_line:
            # Ox axis
            line = Segment(0, lam.Rext * 1.5)
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # Z1 Line
            line = Segment(0, Rbo * 2 * exp(-1j * self.W0 / 2))
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # Z2 Line
            line = Segment(0, Rbo * 2 * exp(1j * self.W0 / 2))
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # Top arc
            line = Arc1(
                begin=point_dict["Z1"],
                end=point_dict["Z4"],
                radius=self.get_Rbo(),
                is_trigo_direction=True,
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # Magnet Arc
            line = Segment(point_dict["Zc"], point_dict["ZM2"])
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            line = Segment(point_dict["Zc"], point_dict["ZM3"])
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )

        if type_add_active == 1:
            self.plot_active(fig=fig, is_show_fig=False)
        elif type_add_active == 2:
            self.plot_active(
                fig=fig, is_show_fig=False, enforced_default_color=MAGNET_COLOR
            )

        # Zooming and cleaning
        W = point_dict["Z4"].imag * 1.2
        Rint, Rext = self.comp_radius()

        plt.axis("equal")
        ax.set_xlim(Rint, Rext)
        ax.set_ylim(-W, W)
        fig.canvas.set_window_title(type(self).__name__ + " Schematics")
        ax.set_title("")
        ax.get_legend().remove()
        ax.set_axis_off()

        # Save / Show
        if save_path is not None:
            fig.savefig(save_path)
            plt.close()

        if is_show_fig:
            fig.show()
