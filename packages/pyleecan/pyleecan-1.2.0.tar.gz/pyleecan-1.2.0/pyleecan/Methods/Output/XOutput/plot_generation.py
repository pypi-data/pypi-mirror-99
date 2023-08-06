import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from ....Methods.Output.XOutput import _get_symbol_data_


def plot_generation(self, x_symbol, y_symbol, ax=None):
    """Plot every fitness values according to the two fitness

    Parameters
    ----------
    self : XOutput
    obj1 : str
        symbol of the ParamExplorer, the OptiObjective or the DataKeeper
    obj2 : str
        symbol of the ParamExplorer, the OptiObjective or the DataKeeper
    """

    # TODO define the colormap according to Pyleecan graphical chart
    # Colormap definition
    cm = LinearSegmentedColormap.from_list(
        "colormap",
        [(35 / 255, 89 / 255, 133 / 255), (250 / 255, 202 / 255, 56 / 255)],
        N=max(self["ngen"].result) + 1,
    )

    # Get fitness and ngen
    is_valid = np.array(self["is_valid"].result)
    ngen = np.array(self["ngen"].result)

    # Keep only valid values
    indx = np.where(is_valid)[0]

    ngen = ngen[indx]

    # get data and labels
    x_values, x_label = _get_symbol_data_(self, x_symbol, indx)
    y_values, y_label = _get_symbol_data_(self, y_symbol, indx)

    if ax is None:
        fig, ax = plt.subplots()

        # Plot fitness values
        scatter = ax.scatter(x_values, y_values, s=8, c=ngen, cmap=cm)

        # Add legend
        legend1 = ax.legend(
            *scatter.legend_elements(), loc="upper right", title="Generation"
        )
        ax.add_artist(legend1)

        # Extend xlim to give some space to the legend
        left, right = ax.get_xlim()
        ax.set_xlim(left, right + 0.2 * abs(right - left))

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title("Fitness values for each individual")
        fig.show()

    else:
        # Plot fitness values
        scatter = ax.scatter(x_values, y_values, s=8, c=ngen, cmap=cm)

        # Add legend
        legend1 = ax.legend(
            *scatter.legend_elements(), loc="upper right", title="Generation"
        )
        ax.add_artist(legend1)

        # Extend xlim to give some space to the legend
        left, right = ax.get_xlim()
        ax.set_xlim(left, right + 0.2 * abs(right - left))

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title("Fitness values for each individual")

        return ax
