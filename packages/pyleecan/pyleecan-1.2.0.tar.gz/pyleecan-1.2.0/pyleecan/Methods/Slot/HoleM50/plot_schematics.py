import matplotlib.pyplot as plt
from numpy import pi, exp

from ....Classes.Arc1 import Arc1
from ....Classes.LamHole import LamHole
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
    self : HoleM50
        A HoleM50 object
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
        hole = type(self)(
            H0=0.01496,
            H1=0.0065,
            H2=0.003,
            H3=0.0085,
            H4=0.004,
            W0=0.042,
            W1=0.005,
            W2=0.004,
            W3=0.007,
            W4=0.0129,
            Zh=8,
        )
        lam = LamHole(
            Rint=0.05532, Rext=0.0812, is_internal=True, is_stator=False, hole=[hole]
        )
        hole.plot_schematics(
            is_default=False,
            is_add_point_label=is_add_point_label,
            is_add_schematics=is_add_schematics,
            is_add_main_line=is_add_main_line,
            type_add_active=type_add_active,
            save_path=save_path,
            is_show_fig=is_show_fig,
        )
    elif type_add_active == 0:
        # Remove magnets
        lam = self.parent.copy()
        lam.hole[0].remove_magnet()
        lam.hole[0].plot_schematics(
            is_default=False,
            is_add_point_label=is_add_point_label,
            is_add_schematics=is_add_schematics,
            is_add_main_line=is_add_main_line,
            type_add_active=2,
            save_path=save_path,
            is_show_fig=is_show_fig,
        )
    else:
        # Getting the main plot
        if self.parent is None:
            raise ParentMissingError("Error: The hole is not inside a Lamination")
        lam = self.parent
        alpha = pi / 2  # To rotate the schematics
        lam.plot(
            alpha=pi / self.Zh + alpha,
            is_show_fig=False,
            is_lam_only=type_add_active == 0,
        )  # center hole on Ox axis
        sp = 2 * pi / self.Zh
        Rbo = self.get_Rbo()
        fig = plt.gcf()
        ax = plt.gca()
        point_dict = self._comp_point_coordinate()

        # Adding point label
        if is_add_point_label:
            for name, Z in point_dict.items():
                Z = Z * exp(1j * alpha)
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
            line = Segment(
                point_dict["Z9"] * exp(1j * alpha), point_dict["Z9s"] * exp(1j * alpha)
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="W0",
                offset_label=self.W0 * 0.3 + 1j * self.H3 * 0.2,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # W1
            line = Segment(
                (point_dict["Z8"] + point_dict["Z7"]) / 2 * exp(1j * alpha),
                (point_dict["Z8s"] + point_dict["Z7s"]) / 2 * exp(1j * alpha),
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="W1",
                offset_label=-1j * self.H3 * 0.4,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # W2
            line = Segment(
                point_dict["Z8"] * exp(1j * alpha), point_dict["Z8b"] * exp(1j * alpha)
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="W2",
                offset_label=1j * self.H3 * 0.2,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # W3
            line = Segment(
                (point_dict["Z1s"] + point_dict["Z11s"]) * 0.5 * exp(1j * alpha),
                (point_dict["Z1"] + point_dict["Z11"])
                * 0.5
                * exp(1j * sp)
                * exp(1j * alpha),
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="W3",
                offset_label=-1j * self.H3 * 0.3,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # W4
            line = Segment(
                point_dict["Z5"] * exp(1j * alpha), point_dict["Z4"] * exp(1j * alpha)
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="W4",
                offset_label=-1j * self.H3 * 0.3,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # H0
            line = Segment(
                Rbo * exp(1j * alpha), point_dict["Z8"].real * exp(1j * alpha)
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="H0",
                offset_label=self.W0 * 0.05 + 1j * self.H3 * 0.2,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # H1
            line = Segment(
                Rbo * exp(-1j * sp / 2) * exp(1j * alpha),
                (Rbo - self.H1) * exp(-1j * sp / 2) * exp(1j * alpha),
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="H1",
                offset_label=self.H3 * 0.2,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # H2
            line = Segment(
                (point_dict["Z3s"] + point_dict["Z6s"]) * 0.5 * exp(1j * alpha),
                (point_dict["Z4s"] + point_dict["Z5s"]) * 0.5 * exp(1j * alpha),
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="H2",
                offset_label=self.H3 * 0.2,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # H3
            line = Segment(
                point_dict["Z4s"] * exp(1j * alpha),
                point_dict["Z8cs"] * exp(1j * alpha),
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="H3",
                offset_label=self.H3 * 0.2,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # H4
            line = Segment(
                point_dict["Z9s"] * exp(1j * alpha),
                point_dict["Z10s"] * exp(1j * alpha),
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="H4",
                offset_label=self.H3 * 0.2,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )

        if is_add_main_line:
            # Ox axis
            line = Segment(0, lam.Rext * 1.5 * exp(1j * alpha))
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # Tooth axis
            line = Segment(0, lam.Rext * 1.5 * exp(1j * sp / 2) * exp(1j * alpha))
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            line = Segment(0, lam.Rext * 1.5 * exp(-1j * sp / 2) * exp(1j * alpha))
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # H1 radius
            line = Arc1(
                begin=(Rbo - self.H1) * exp(-1j * pi / 2 * 0.9) * exp(1j * alpha),
                end=(Rbo - self.H1) * exp(1j * pi / 2 * 0.9) * exp(1j * alpha),
                radius=Rbo - self.H1,
                is_trigo_direction=True,
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # H4 radius
            line = Arc1(
                begin=(Rbo - self.H1 + self.H4)
                * exp(-1j * pi / 2 * 0.9)
                * exp(1j * alpha),
                end=(Rbo - self.H1 + self.H4)
                * exp(1j * pi / 2 * 0.9)
                * exp(1j * alpha),
                radius=Rbo - self.H1 + self.H4,
                is_trigo_direction=True,
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # W1 lines
            line = Segment(
                point_dict["Z7"] * exp(1j * alpha), point_dict["Z7s"] * exp(1j * alpha)
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            line = Segment(
                point_dict["Z8"] * exp(1j * alpha), point_dict["Z8s"] * exp(1j * alpha)
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # W2 lines
            line = Segment(
                point_dict["Z8"] * exp(1j * alpha), point_dict["Z8a"] * exp(1j * alpha)
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            line = Segment(
                point_dict["Z8s"] * exp(1j * alpha),
                point_dict["Z8as"] * exp(1j * alpha),
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # H2 lines
            line = Segment(
                point_dict["Z3s"] * exp(1j * alpha), point_dict["Z6s"] * exp(1j * alpha)
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )

        # Zooming and cleaning
        W = abs(point_dict["Z11s"].imag) * 1.3
        Rint = self.parent.Rint
        Rext = self.parent.Rext

        plt.axis("equal")
        ax.set_ylim(Rint, Rext)
        ax.set_xlim(-W, W)
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
