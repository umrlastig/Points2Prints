from pathlib import Path
from typing import List

import geopandas as gpd
import pandas as pd

from ..utils import (
    InputOutput,
    LoggingContext,
    OutputActionEnum,
    OutputBehaviour,
    Verbose,
    read_polygon_dataset,
    write_polygon_dataset,
)


def merge_polygons_implementation(
    input_files: List[Path],
    output_file: Path,
    input_output: InputOutput,
):
    input_output.handle_input(
        message_prefix="Merge polygons",
        input_files=input_files,
    )
    output_action = input_output.handle_output(
        message_prefix="Merge polygons",
        behaviour=OutputBehaviour.ALL_OR_NOTHING,
        output_files=[[output_file]],
    )
    if output_action == OutputActionEnum.SKIP:
        return

    input_polygons = [read_polygon_dataset(input_file) for input_file in input_files]

    # Check if all files have the same CRS
    crs_list = list(map(lambda x: x.crs, input_polygons))
    if len(set(crs_list)) != 1:
        raise ValueError("All input files must have the same CRS.")
    crs = crs_list[0]

    merged_polygons = gpd.GeoDataFrame(pd.concat(input_polygons))

    write_polygon_dataset(merged_polygons, output_file, crs=crs)


def merge_polygons_call(
    input_files: List[Path],
    output_file: Path,
    input_output: InputOutput,
    verbose: Verbose,
):
    with LoggingContext(verbose=verbose):
        return merge_polygons_implementation(
            input_files=input_files,
            output_file=output_file,
            input_output=input_output,
        )
