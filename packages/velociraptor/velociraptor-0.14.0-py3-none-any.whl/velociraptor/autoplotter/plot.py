"""
Functions that actually plot x against y.
"""

import matplotlib.pyplot as plt
import numpy as np
import unyt

from matplotlib import rcParams

from matplotlib.colors import LogNorm
from velociraptor import VelociraptorCatalogue
from velociraptor.autoplotter.objects import VelociraptorLine
from typing import Tuple, Union

import velociraptor.tools as tools


def scatter_x_against_y(
    x: unyt.unyt_array, y: unyt.unyt_array
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Creates a scatter of x against y (unyt arrays).
    """

    fig, ax = plt.subplots()

    kwargs = dict(edgecolor="none", zorder=-100)

    # Need to "intelligently" size the markers
    kwargs["s"] = (
        rcParams["lines.markersize"]
        * (6.0 - 5.0 * np.tanh(0.75 * np.log10(x.size) - 3.0))
        / 11.0
    )

    kwargs["alpha"] = (5.5 - 4.5 * np.tanh(0.75 * np.log10(x.size) - 3.0)) / 10.0

    ax.scatter(x.value, y.value, **kwargs)

    return fig, ax


def histogram_x_against_y(
    x: unyt.unyt_array,
    y: unyt.unyt_array,
    x_bins: unyt.unyt_array,
    y_bins: unyt.unyt_array,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Creates a plot of x against y with a 2d histogram in the background.
    
    Actually uses pcolormesh and the numpy histogram method.
    """

    fig, ax = plt.subplots()

    H, x_bins, y_bins = np.histogram2d(x=x, y=y, bins=[x_bins, y_bins])

    im = ax.pcolormesh(
        x_bins, y_bins, H.T, norm=LogNorm(vmin=1, vmax=max(H.max(), 1)), zorder=-100
    )

    fig.colorbar(im, ax=ax, label="Number of haloes", pad=0.0)

    return fig, ax


def mass_function(
    x: unyt.unyt_array, x_bins: unyt.unyt_array, mass_function: VelociraptorLine
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Creates a plot of x as a mass function, binned with x_bins.
    """

    fig, ax = plt.subplots()

    if mass_function.adaptive_mass_function:
        centers, mass_function, error, *_ = mass_function.output
        ax.errorbar(
            centers, mass_function, yerr=error, xerr=abs(x_bins - centers), fmt=".",
        )
    else:
        centers, mass_function, error, *_ = mass_function.output
        ax.errorbar(centers, mass_function, error)

    return fig, ax


def histogram(
    x: unyt.unyt_array, x_bins: unyt.unyt_array, histogram: VelociraptorLine
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Creates a plot of x as a mass function, binned with x_bins.
    """

    fig, ax = plt.subplots()

    centers, mass_function, *_ = histogram.output

    ax.plot(centers, mass_function)

    return fig, ax


def decorate_axes(
    ax: plt.Axes,
    catalogue: VelociraptorCatalogue,
    comment: Union[str, None] = None,
    legend_loc: str = "upper left",
    redshift_loc: str = "lower right",
    comment_loc: str = "lower left",
) -> None:
    """
    Decorates the axes with information about the redshift and
    scale-factor.
    """

    markerfirst = "right" not in legend_loc

    if len(ax.get_legend_handles_labels()[0]):
        # Only create the legend if we have handles available to plot,
        # otherwise we get a warning from matplotlib printed to the
        # console.
        legend = ax.legend(loc=legend_loc, markerfirst=markerfirst)
        fontsize = legend.get_texts()[0].get_fontsize()
    else:
        fontsize = None

    label_switch = {
        redshift_loc: f"$z={catalogue.z:2.3f}$\n$a={catalogue.a:2.3f}$",
        comment_loc: comment,
    }

    distance_from_edge = 0.025

    for loc, label in label_switch.items():
        if label is not None:
            # First need to parse the 'loc' string
            try:
                va, ha = loc.split(" ")
            except ValueError:
                if loc == "right":
                    ha = "right"
                    va = "center"
                elif loc == "center":
                    ha = "center"
                    va = "center"

            if va == "lower":
                y = distance_from_edge
                va = "bottom"
            elif va == "upper":
                y = 1.0 - distance_from_edge
                va = "top"
            elif va == "center":
                y = 0.5
            else:
                raise AttributeError(
                    f"Unknown location string {loc}. Choose e.g. lower right"
                )

            if ha == "left":
                x = distance_from_edge
            elif ha == "right":
                x = 1.0 - distance_from_edge
            elif ha == "center":
                x = 0.5

            ax.text(
                x,
                y,
                label,
                ha=ha,
                va=va,
                transform=ax.transAxes,
                multialignment=ha,
                fontsize=fontsize,
            )

    return


def get_labels(x: unyt.unyt_array, y: unyt.unyt_array, mass_function: bool) -> None:
    """
    Set the x and y labels for the axes.
    """

    x_label = tools.get_full_label(x)
    y_label = (
        tools.get_mass_function_label(
            mass_function_sub_label="{}", mass_function_units=y.units
        )
        if mass_function
        else tools.get_full_label(y)
    )

    return x_label, y_label
