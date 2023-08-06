"""
Functions for plotting rose plots.
"""

import math
from textwrap import wrap
from typing import Dict, Optional, Tuple, Union

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.projections import PolarAxes


def _calc_ideal_bin_width(n: Union[int, float], axial=True) -> float:
    """
    Calculate ideal bin width. axial or vector data.

    Reference:
        Sanderson, D.J., Peacock, D.C.P., 2020.
        Making rose diagrams fit-for-purpose. Earth-Science Reviews.
        doi:10.1016/j.earscirev.2019.103055

    E.g.

    >>> _calc_ideal_bin_width(30)
    28.964681538168897

    >>> _calc_ideal_bin_width(90)
    20.08298850246509

    :param n: Sample size
    :type n: int
    :param axial: Whether data is axial or vector
    :type axial: bool
    :return: Bin width in degrees
    :rtype: float
    :raises: ValueError
    """
    if n <= 0:
        raise ValueError("Sample size cannot be 0 or lower")
    if axial:
        degree_range = 180
    else:
        degree_range = 360
    return degree_range / (2 * n ** (1 / 3))


def _calc_bins(ideal_bin_width: float) -> Tuple[np.ndarray, float]:
    """
    Calculate bin edges and real bin width from ideal bin width.

    E.g.

    >>> _calc_bins(25.554235)
    (array([  0. ,  22.5,  45. ,  67.5,  90. , 112.5, 135. , 157.5, 180. ]), 22.5)
    """
    div = 180 / ideal_bin_width
    rounded_div = math.ceil(div)
    bin_width = 180 / rounded_div

    start = 0
    end = 180 + bin_width * 0.01
    bin_edges = np.arange(start, end, bin_width)
    return bin_edges, bin_width


def _calc_locs(bin_width: float) -> np.ndarray:
    """
    Calculate bar plot bar locations.

    E.g.

    >>> _calc_locs(15)
    array([  7.5,  22.5,  37.5,  52.5,  67.5,  82.5,  97.5, 112.5, 127.5,
           142.5, 157.5, 172.5])

    :param bin_width: Real bin width
    :type bin_width: float
    :return: Array of locations
    :rtype: np.ndarray
    """
    start = bin_width / 2
    end = 180 + bin_width / 2
    locs = np.arange(start, end, bin_width)
    return locs


def determine_azimuth_bins(
    azimuth_array: np.ndarray,
    length_array: Optional[np.ndarray] = None,
    bin_multiplier: Union[float, int] = 1,
) -> Dict[str, np.ndarray]:
    """
    Calculate azimuth bins for plotting azimuth rose plots.

    E.g.

    >>> from pprint import pprint
    >>> azimuth_array = np.array([25, 50, 145, 160])
    >>> length_array = np.array([5, 5, 10, 60])
    >>> pprint(determine_azimuth_bins(azimuth_array, length_array))
    {'bin_heights': array([ 5,  5,  0, 70]),
     'bin_locs': array([ 22.5,  67.5, 112.5, 157.5]),
     'bin_width': 45.0}

    """
    # Ideal width of rose plot bin based on sample size.
    # Lower bin size with bin_multiplier (result no longer ideal!)
    ideal_bin_width = _calc_ideal_bin_width(len(azimuth_array))
    ideal_bin_width = ideal_bin_width * bin_multiplier
    # True rose plot width.
    bin_edges, bin_width = _calc_bins(ideal_bin_width)
    # Location of rose plot bins.
    bin_locs = _calc_locs(bin_width)
    if length_array is None:
        # If no length_array is passed weight of 1.0 for all means equal
        # weights.
        length_array = np.array([1.0] * (len(azimuth_array)))
    # Height of rose plot bins.
    bin_heights, _ = np.histogram(azimuth_array, bin_edges, weights=length_array)

    return dict(bin_width=bin_width, bin_locs=bin_locs, bin_heights=bin_heights)


def plot_azimuth_ax(
    bin_width: float,
    bin_locs: np.ndarray,
    bin_heights: np.ndarray,
    ax: PolarAxes,  # type: ignore
):
    """
    Plot azimuth rose plot to ax.
    """
    # Rose type always equal-area
    number_of_azimuths = np.sqrt(bin_heights)

    # Plot azimuth rose plot
    ax.bar(
        np.deg2rad(bin_locs),
        number_of_azimuths,
        width=np.deg2rad(bin_width),
        bottom=0.0,
        color="darkgrey",
        edgecolor="k",
        alpha=0.85,
        zorder=4,
    )

    # Plot setup
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_thetagrids(
        np.arange(0, 181, 45),
        fontweight="bold",
        fontfamily="DejaVu Sans",
        fontsize=11,
        alpha=0.95,
    )
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    # The average of number_of_azimuths is displayed as a radial grid-line.
    # TODO: Cannot modify theta lines or r lines
    _, _ = ax.set_rgrids(
        radii=(number_of_azimuths.mean(),),  # type: ignore
        angle=0,
        fontsize=1,
        alpha=0.8,
        fmt="",
        ha="left",
    )
    # TODO: No effect
    # if isinstance(rlines, list):
    #     rline: plt.Line2D
    #     for rline in rlines:
    #         rline.set_linestyle("dashed")
    #         rline.set_linewidth(1)
    #         rline.set_color("black")

    # Tick labels
    labels = ax.get_xticklabels()
    for label in labels:
        label._y = -0.03
        label._fontproperties._size = 15
        label._fontproperties._weight = "bold"
    return ax


def _create_azimuth_set_text(
    length_array: np.ndarray, set_array: np.ndarray, set_names: Tuple[str, ...]
) -> str:
    """
    Create azimuth set statistics for figure.

    E.g.

    >>> length_array = np.array([5, 5, 10, 60])
    >>> set_array = np.array([str(val) for val in [1, 1, 2, 2]])
    >>> set_names = ["1", "2"]
    >>> print(_create_azimuth_set_text(length_array, set_array, set_names))
    Set 1, FoL = 12.5%
    Set 2, FoL = 87.5%

    """
    sum_length = length_array.sum()
    t = ""
    for idx, set_name in enumerate(set_names):
        total_length = sum(length_array[set_array == set_name])
        percent = total_length / sum_length
        text = "Set {}, FoL = {}".format(set_name, "{:.1%}".format(percent))

        if idx < len(set_names) - 1:
            text = text + "\n"
        t = t + text
    return t


def decorate_azimuth_ax(
    ax: Axes,
    label: str,
    length_array: np.ndarray,
    set_array: np.ndarray,
    set_names: Tuple[str, ...],
):
    """
    Decorate azimuth rose plot ax.
    """
    # Title is the name of the target area or group
    prop_title = dict(boxstyle="square", facecolor="linen", alpha=1, linewidth=2)
    title = "\n".join(wrap(f"{label}", 10))
    ax.set_title(
        title,
        x=0.94,
        y=0.8,
        fontsize=20,
        fontweight="bold",
        fontfamily="DejaVu Sans",
        va="top",
        bbox=prop_title,
        transform=ax.transAxes,
        ha="center",
    )
    prop = dict(boxstyle="square", facecolor="linen", alpha=1, pad=0.45)
    text = f"n ={len(set_array)}\n"
    text = text + _create_azimuth_set_text(length_array, set_array, set_names)
    ax.text(
        0.94,
        0.3,
        text,
        transform=ax.transAxes,
        fontsize=12,
        weight="roman",
        bbox=prop,
        fontfamily="DejaVu Sans",
        va="top",
        ha="center",
    )


def plot_azimuth_plot(
    azimuth_array: np.ndarray,
    length_array: np.ndarray,
    azimuth_set_array: np.ndarray,
    azimuth_set_names: Tuple[str, ...],
    label: str,
) -> Tuple[Dict[str, np.ndarray], Figure, Axes]:
    """
    Plot azimuth rose plot to its own figure.

    Returns rose plot bin parameters, figure, ax
    """
    azimuth_bin_dict = determine_azimuth_bins(azimuth_array, length_array)
    fig, ax = plt.subplots(subplot_kw=dict(polar=True), figsize=(6.5, 5.1))
    ax = plot_azimuth_ax(**azimuth_bin_dict, ax=ax)
    # TODO: Is length_array always required
    decorate_azimuth_ax(
        ax=ax,
        label=label,
        length_array=length_array,
        set_array=azimuth_set_array,
        set_names=azimuth_set_names,
    )
    return (
        azimuth_bin_dict,
        fig,
        ax,
    )
