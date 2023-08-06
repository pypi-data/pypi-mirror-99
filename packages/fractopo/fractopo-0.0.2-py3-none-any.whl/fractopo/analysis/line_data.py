"""
Trace and branch data analysis with LineData class abstraction.
"""
import logging
from dataclasses import dataclass
from typing import Dict, Literal, Optional, Tuple

import geopandas as gpd
import numpy as np
import powerlaw
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from fractopo import SetRangeTuple
from fractopo.analysis import azimuth, length_distributions, parameters
from fractopo.general import (
    Col,
    determine_azimuth,
    determine_set,
    intersection_count_to_boundary_weight,
    numpy_to_python_type,
)

# Math and analysis imports
# Plotting imports
# DataFrame analysis imports


# Own code imports


def _column_array_property(
    column: Literal[
        Col.AZIMUTH,
        Col.LENGTH,
        Col.AZIMUTH_SET,
        Col.LENGTH_SET,
        Col.LENGTH_WEIGHTS,
        Col.LENGTH_NON_WEIGHTED,
    ],
    gdf: gpd.GeoDataFrame,
) -> Optional[np.ndarray]:
    if column.value in gdf:
        return gdf[column.value].to_numpy()
    else:
        return None


@dataclass
class LineData:

    """
    Wrapper around the given line_gdf (trace or branch data).

    The line_gdf reference is passed and LineData will modify the input
    line_gdf instead of copying the input frame. This means line_gdf columns
    are accesible in the passed input reference upstream.
    """

    line_gdf: gpd.GeoDataFrame

    azimuth_set_ranges: SetRangeTuple
    azimuth_set_names: Tuple[str, ...]

    length_set_ranges: Optional[SetRangeTuple]
    length_set_names: Optional[Tuple[str, ...]]

    area_boundary_intersects: Optional[np.ndarray]

    _automatic_fit: Optional[powerlaw.Fit] = None

    @property
    def azimuth_array(self):
        """
        Array of trace or branch azimuths.
        """
        column_array = _column_array_property(column=Col.AZIMUTH, gdf=self.line_gdf)
        if column_array is None:
            column_array = np.array(
                [
                    determine_azimuth(line, halved=True)
                    for line in self.line_gdf.geometry
                ]
            )
            self.line_gdf[Col.AZIMUTH.value] = column_array
        return column_array

    @property
    def azimuth_set_array(self):
        """
        Array of trace or branch azimuth set ids.
        """
        column_array = _column_array_property(column=Col.AZIMUTH_SET, gdf=self.line_gdf)
        if column_array is None:
            column_array = np.array(
                [
                    determine_set(
                        azimuth,
                        self.azimuth_set_ranges,
                        self.azimuth_set_names,
                        loop_around=True,
                    )
                    for azimuth in self.azimuth_array
                ]
            )
            self.line_gdf[Col.AZIMUTH_SET.value] = column_array
        return column_array

    @property
    def length_boundary_weights(self):
        """
        Array of weights for lines based on intersection count with boundary.
        """
        column_array = _column_array_property(
            column=Col.LENGTH_WEIGHTS, gdf=self.line_gdf
        )
        if column_array is None:
            assert self.area_boundary_intersects.dtype in ("int64", "float64")
            column_array = np.array(
                [
                    intersection_count_to_boundary_weight(int(inter_count))
                    for inter_count in self.area_boundary_intersects
                ]
            )
            self.line_gdf[Col.LENGTH_WEIGHTS.value] = column_array
        return column_array

    @property
    def length_array_non_weighted(self):
        """
        Array of trace or branch lengths not weighted by boundary conditions.
        """
        column_array = _column_array_property(
            column=Col.LENGTH_NON_WEIGHTED, gdf=self.line_gdf
        )
        if column_array is None:
            column_array = self.line_gdf.geometry.length.to_numpy()
            self.line_gdf[Col.LENGTH_NON_WEIGHTED.value] = column_array
        return column_array

    @property
    def length_array(self):
        """
        Array of trace or branch lengths.
        """
        column_array = _column_array_property(column=Col.LENGTH, gdf=self.line_gdf)
        if column_array is None:
            column_array = (
                self.line_gdf.geometry.length.to_numpy() * self.length_boundary_weights
                if self.area_boundary_intersects is not None
                else 1.0
            )
            self.line_gdf[Col.LENGTH.value] = column_array
        return column_array

    @property
    def length_set_array(self) -> Optional[np.ndarray]:
        """
        Array of trace or branch length set ids.
        """
        if self.length_set_names is None or self.length_set_ranges is None:
            logging.error("Expected length_set_names and _ranges to be defined.")
            return None
        column_array = _column_array_property(column=Col.LENGTH_SET, gdf=self.line_gdf)
        if column_array is None:
            column_array = np.array(
                [
                    determine_set(
                        length,
                        self.length_set_ranges,
                        self.length_set_names,
                        loop_around=False,
                    )
                    for length in self.length_array
                ]
            )
            self.line_gdf[Col.LENGTH_SET.value] = column_array
        return column_array

    @property
    def azimuth_set_counts(self) -> Dict[str, int]:
        """
        Get dictionary of azimuth set counts.
        """
        return parameters.determine_set_counts(
            self.azimuth_set_names, self.azimuth_set_array
        )

    @property
    def length_set_counts(self) -> Dict[str, int]:
        """
        Get dictionary of length set counts.
        """
        return parameters.determine_set_counts(
            self.length_set_names, self.length_set_array
        )

    @property
    def automatic_fit(self) -> powerlaw.Fit:
        """
        Get automatic powerlaw Fit.
        """
        if self._automatic_fit is None:
            self._automatic_fit = length_distributions.determine_fit(self.length_array)
        return self._automatic_fit

    @property
    def boundary_intersect_count(self) -> Optional[Dict[str, int]]:
        """
        Get counts of line intersects with boundary.
        """
        if not isinstance(self.area_boundary_intersects, np.ndarray):
            return None
        keys, counts = np.unique(self.area_boundary_intersects, return_counts=True)
        keys = list(map(str, keys))
        counts = list(map(numpy_to_python_type, counts))
        key_counts = dict(zip(keys, counts))
        return key_counts

    def determine_manual_fit(self, cut_off: float) -> powerlaw.Fit:
        """
        Get manually determined Fit with set cut off.
        """
        return length_distributions.determine_fit(self.length_array, cut_off=cut_off)

    def cut_off_proportion_of_data(self, fit: Optional[powerlaw.Fit] = None) -> float:
        """
        Get the proportion of data cut off by `powerlaw` cut off.

        If no fit is passed the cut off is the one used in `automatic_fit`.
        """
        fit = self.automatic_fit if fit is None else fit
        return (
            sum(self.length_array < fit.xmin) / len(self.length_array)
            if len(self.length_array) > 0
            else 0.0
        )

    def describe_fit(self, label: Optional[str] = None):
        """
        Return short description of automatic powerlaw fit.
        """
        return length_distributions.describe_powerlaw_fit(
            self.automatic_fit, label=label
        )

    def plot_lengths(
        self,
        label: str,
        fit: Optional[powerlaw.Fit] = None,
    ) -> Tuple[powerlaw.Fit, Figure, Axes]:
        """
        Plot length data with powerlaw fit.
        """
        return length_distributions.plot_distribution_fits(
            self.length_array,
            label=label,
            fit=self.automatic_fit if fit is None else fit,
        )

    def plot_azimuth(self, label: str) -> Tuple[Dict[str, np.ndarray], Figure, Axes]:
        """
        Plot azimuth data in rose plot.
        """
        return azimuth.plot_azimuth_plot(
            self.azimuth_array,
            self.length_array,
            self.azimuth_set_array,
            self.azimuth_set_names,
            label=label,
        )

    def plot_azimuth_set_count(self, label: str) -> Tuple[Figure, Axes]:
        """
        Plot azimuth set counts.
        """
        return parameters.plot_set_count(self.azimuth_set_counts, label=label)

    def plot_length_set_count(self, label: str) -> Tuple[Figure, Axes]:
        """
        Plot length set counts.
        """
        return parameters.plot_set_count(self.length_set_counts, label=label)
