import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.affinity import translate

from ..utils import (
    InputOutput,
    LoggingContext,
    OutputActionEnum,
    OutputBehaviour,
    Verbose,
    read_polygon_dataset,
    write_polygon_dataset,
)


def align_centroids_implementation(
    input_file: Path,
    reference_file: Path,
    output_file: Path,
    key: str,
    input_output: InputOutput,
):
    input_output.handle_input(
        message_prefix="Align centroids",
        input_files=[input_file, reference_file],
    )
    output_action = input_output.handle_output(
        message_prefix="Align centroids",
        behaviour=OutputBehaviour.ALL_OR_NOTHING,
        output_files=[[output_file]],
    )
    if output_action == OutputActionEnum.SKIP:
        return

    columns = [key, "geometry"]
    input_data = read_polygon_dataset(input_file=input_file, columns=columns)
    reference_data = read_polygon_dataset(input_file=reference_file, columns=columns)
    input_crs = input_data.crs
    reference_crs = reference_data.crs

    if input_crs != reference_crs:
        raise ValueError("The input and reference datasets have different CRS.")
    crs = input_crs
    if crs == None:
        raise ValueError("The input dataset is missing CRS information.")

    # Merge the two datasets keeping only the shared entities
    merged_data = gpd.GeoDataFrame(
        pd.merge(
            input_data,
            reference_data,
            how="inner",
            left_on=key,
            right_on=key,
            suffixes=("_old", "_ref"),
        )
    )

    # Compute the centroid of the merged entities
    merged_data["centroid_old"] = merged_data["geometry_old"].centroid
    merged_data["centroid_ref"] = merged_data["geometry_ref"].centroid

    # Translate the old entity to align its centroid to the reference
    merged_data["geometry_new"] = merged_data.apply(
        lambda row: translate(
            row["geometry_old"],
            xoff=float(row["centroid_ref"].x - row["centroid_old"].x),
            yoff=float(row["centroid_ref"].y - row["centroid_old"].y),
        ),
        axis=1,
    )

    # Select only the new geometries with the key
    merged_data = merged_data[[key, "geometry_new"]]
    merged_data.rename(columns={"geometry_new": "geometry"}, inplace=True)
    merged_data.geometry.set_crs(crs, inplace=True)

    write_polygon_dataset(dataset=merged_data, output_file=output_file, crs=crs)


def align_centroids_call(
    input_file: Path,
    reference_file: Path,
    output_file: Path,
    key: str,
    input_output: InputOutput,
    verbose: Verbose,
):
    with LoggingContext(verbose=verbose):
        return align_centroids_implementation(
            input_file=input_file,
            reference_file=reference_file,
            output_file=output_file,
            key=key,
            input_output=input_output,
        )
