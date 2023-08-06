# -*- coding: utf-8 -*-

from .plot_4D import plot_4D
from .plot_3D import plot_3D
from . import unit_dict, norm_dict, axes_dict
from numpy import where, meshgrid, max as np_max, min as np_min


def plot_3D_Data(
    data,
    *arg_list,
    is_norm=False,
    unit="SI",
    save_path=None,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
    z_range=None,
    is_auto_ticks=True,
    is_2D_view=False,
    N_stem=100,
    fig=None,
    ax=None,
    is_show_fig=None,
):
    """Plots a field as a function of two axes

    Parameters
    ----------
    data : Data
        a Data object
    *arg_list : list of str
        arguments to specify which axes to plot
    is_norm : bool
        boolean indicating if the field must be normalized
    unit : str
        unit in which to plot the field
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    x_min : float
        minimum value for the x-axis
    x_max : float
        maximum value for the x-axis
    y_min : float
        minimum value for the y-axis
    y_max : float
        maximum value for the y-axis
    z_min : float
        minimum value for the z-axis
    z_max : float
        maximum value for the z-axis
    z_range : float
        range to use for the z-axis
    is_auto_ticks : bool
        in fft, adjust ticks to freqs (deactivate if too close)
    is_2D_view : bool
        True to plot Data in xy plane and put z as colormap
    N_stem : int
        number of harmonics to plot (only for stem plots)
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data
    is_show_fig : bool
        True to show figure after plot
    """

    if len(arg_list) == 1 and type(arg_list[0]) == tuple:
        arg_list = arg_list[0]  # if called from another script with *arg_list

    # Set unit
    if unit == "SI":
        unit = data.unit

    # Detect fft
    is_fft = False
    if any("wavenumber" in s for s in arg_list) or any("freqs" in s for s in arg_list):
        is_fft = True
        if "dB" in unit:
            unit_str = (
                "[" + unit + " re. " + str(data.normalizations["ref"]) + data.unit + "]"
            )
        else:
            unit_str = "[" + unit + "]"
        if data.symbol == "Magnitude":
            zlabel = "Magnitude " + unit_str
        else:
            zlabel = r"$|\widehat{" + data.symbol + "}|$ " + unit_str
        title1 = "FFT2 of " + data.name.lower() + " "
    else:
        if is_norm:
            zlabel = (
                r"$\frac{" + data.symbol + "}{" + data.symbol + "_0}\, [" + unit + "]$"
            )
        else:
            zlabel = r"$" + data.symbol + "\, [" + unit + "]$"
        title1 = "Surface plot of " + data.name.lower() + " "

    # Extract field and axes
    if is_fft:
        if is_2D_view:
            result = data.get_magnitude_along(arg_list, unit=unit, is_norm=is_norm)
        else:
            result = data.get_harmonics(
                N_stem, arg_list, unit=unit, is_norm=is_norm, is_flat=True
            )
    else:
        result = data.get_along(arg_list, unit=unit, is_norm=is_norm)
    axes_list = result["axes_list"]
    axes_dict_other = result["axes_dict_other"]
    Xdata = result[axes_list[0].name]
    Ydata = result[axes_list[1].name]
    Zdata = result[data.symbol]
    if is_fft and not is_2D_view:
        X_flat = Xdata
        Y_flat = Ydata
        Z_flat = Zdata

    else:
        Y_map, X_map = meshgrid(Ydata, Xdata)
        X_flat = X_map.flatten()
        Y_flat = Y_map.flatten()
        Z_flat = Zdata.flatten()
    if x_min is None:
        x_min = np_min(Xdata)
    if x_max is None:
        x_max = np_max(Xdata)
    if y_min is None:
        y_min = np_min(Ydata)
    if y_max is None:
        y_max = np_max(Ydata)
    if z_range is None:
        if z_min is None:
            z_min = np_min(Zdata)
        if z_max is None:
            z_max = np_max(Zdata)
    else:
        if z_min is None and z_max is None:
            z_max = np_max(Zdata)
        if z_max is None:
            z_max = z_min + z_range
        if z_min is None:
            z_min = z_max - z_range

    # Build labels and titles
    axis = axes_list[0]
    if axis.name in axes_dict:
        name = axes_dict[axis.name]
    else:
        name = axis.name
    title2 = "over " + axis.name.lower()
    if axis.unit == "SI":
        unit = unit_dict[axis.name]
        xlabel = name.capitalize() + " [" + unit + "]"
    elif axis.unit in norm_dict:
        xlabel = norm_dict[axis.unit]
    else:
        unit = axis.unit
        xlabel = name.capitalize() + " [" + unit + "]"
    if (
        axis.name == "angle"
        and axis.unit == "°"
        and round(np_max(axis.values) / 6) % 5 == 0
    ):
        xticks = [i * round(np_max(axis.values) / 6) for i in range(7)]
    else:
        xticks = None

    axis = axes_list[1]
    if axis.name in axes_dict:
        name = axes_dict[axis.name]
    else:
        name = axis.name
    title3 = " and " + axis.name.lower()
    if axis.unit == "SI":
        unit = unit_dict[axis.name]
        ylabel = name.capitalize() + " [" + unit + "]"
    elif axis.unit in norm_dict:
        ylabel = norm_dict[axis.unit]
    else:
        unit = axis.unit
        ylabel = name.capitalize() + " [" + unit + "]"
    if (
        axis.name == "angle"
        and axis.unit == "°"
        and round(np_max(axis.values) / 6) % 5 == 0
    ):
        yticks = [i * round(np_max(axis.values) / 6) for i in range(7)]
    else:
        yticks = None

    title4 = ""
    for axis in axes_list[2:]:
        if axis.unit == "SI":
            unit = unit_dict[axis.name]
        elif axis.unit in norm_dict:
            unit = norm_dict[axis.unit]
        else:
            unit = axis.unit
        title4 = " for " + axis.name + "=" + str(result[axis.name]) + " " + unit + ", "
    title5 = ""
    for axis_name in axes_dict_other:
        title5 += (
            axis_name
            + "="
            + str(axes_dict_other[axis_name][0])
            + " "
            + axes_dict_other[axis_name][1]
            + ", "
        )

    if title4 == " for " and title5 == "":
        title4 = ""

    title = title1 + title2 + title3 + title4 + title5
    title = title.rstrip(", ")

    # Call generic plot function
    if is_fft:
        if is_auto_ticks:
            indices = where(Z_flat > abs(0.01 * z_max))[0]
            xticks = X_flat[indices]
            yticks = Y_flat[indices]
        else:
            xticks = None
            yticks = None
        if is_2D_view:
            plot_4D(
                X_flat,
                Y_flat,
                Z_flat,
                is_same_size=True,
                z_max=z_max,
                z_min=z_min,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                zlabel=zlabel,
                fig=fig,
                ax=ax,
                type="scatter",
                save_path=save_path,
                is_show_fig=is_show_fig,
            )
        else:
            plot_3D(
                X_flat,
                Y_flat,
                Z_flat,
                fig=fig,
                ax=ax,
                x_min=x_min,
                x_max=x_max,
                y_min=y_max,
                y_max=y_min,
                z_min=z_min,
                z_max=z_max,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                zlabel=zlabel,
                type="stem",
                save_path=save_path,
                is_show_fig=is_show_fig,
            )
    else:
        if is_2D_view:
            plot_3D(
                X_map,
                Y_map,
                Zdata,
                z_max=z_max,
                z_min=z_min,
                xlabel=xlabel,
                ylabel=ylabel,
                zlabel=zlabel,
                title=title,
                xticks=xticks,
                fig=fig,
                ax=ax,
                type="pcolor",
                save_path=save_path,
                is_show_fig=is_show_fig,
            )
        else:
            plot_3D(
                X_map,
                Y_map,
                Zdata,
                fig=fig,
                ax=ax,
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                z_min=z_min,
                z_max=z_max,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                zlabel=zlabel,
                yticks=yticks,
                type="surf",
                save_path=save_path,
                is_show_fig=is_show_fig,
            )
