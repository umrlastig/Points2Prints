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
)


def _read_polygon_dataset(input_file: Path) -> gpd.GeoDataFrame:
    suffix = input_file.suffix.lower()
    if suffix == ".parquet":
        return gpd.read_parquet(input_file)
    elif suffix in {".gpkg", ".geojson", ".json", ".shp"}:
        return gpd.read_file(input_file)
    else:
        raise ValueError(
            f"Unsupported polygon dataset format for {input_file}. Expected .parquet or .gpkg."
        )


def _write_polygon_dataset(dataset: gpd.GeoDataFrame, output_file: Path) -> None:
    suffix = output_file.suffix.lower()
    if suffix == ".parquet":
        dataset.to_parquet(
            output_file,
            index=False,
            write_covering_bbox=True,
            schema_version="1.1.0",
        )
    elif suffix in {".gpkg", ".geojson", ".json", ".shp"}:
        dataset.to_file(output_file, index=False)
    else:
        raise ValueError(
            f"Unsupported polygon dataset format for {output_file}. Expected .parquet or .gpkg."
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

    input_polygons = [_read_polygon_dataset(input_file) for input_file in input_files]

    merged_polygons = gpd.GeoDataFrame(pd.concat(input_polygons))

    _write_polygon_dataset(merged_polygons, output_file)


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
