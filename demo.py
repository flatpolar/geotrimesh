from pathlib import Path
import geopandas as gpd
from geotrimesh import GeoSceneSet
import tempfile
import os
import logging
import argparse

logging.basicConfig(level=logging.INFO)

out_dirpath = Path(os.getcwd(), "data")

if not os.path.isdir(out_dirpath):
    os.makedirs(out_dirpath)

demodata_dirpath = Path(os.getcwd(), "demodata")
boundary_filepath = Path(demodata_dirpath, "bbox.gpkg")
buildings_filepaths = [Path(demodata_dirpath, "zurich_lod2_clip.glb")]

dem_filepaths = [Path(demodata_dirpath, "dtm_26830_12470_clip_lq.tif")]
ortho_filepaths = [Path(demodata_dirpath, "2507_clip.tif")]
trees_filepaths = []

boundary = gpd.read_file(boundary_filepath).dissolve().explode(index_parts=True)
zurich = GeoSceneSet()

tilingscheme = GeoSceneSet.TilingScheme(boundary, dem_filepaths, height=32, width=32)
tilingscheme.gdf.to_file(Path(out_dirpath, "tiles.gpkg"))

zurich.terrain = GeoSceneSet.Terrain(
    out_dirpath=out_dirpath,
    filepaths=dem_filepaths,
    tiles=tilingscheme.tiles[0:4],
    boundary=boundary
)

zurich.buildings = GeoSceneSet.Features(
    "buildings",
    tilingscheme=tilingscheme,
    out_dirpath=out_dirpath,
    filepaths=buildings_filepaths,
    recombine_bodies=True,
    boundary=boundary,
    extent_orig=[2677116.375000, 1241839.025000, 2689381.985000, 1254150.950000],
    tiles=tilingscheme.tiles[0:4],
)

zurich.ortho = GeoSceneSet.Ortho(
    tilingscheme=tilingscheme,
    out_dirpath=out_dirpath,
    filepaths=ortho_filepaths,
    boundary=boundary,
    tiles=tilingscheme.tiles[0:4],
    include_texture=False
)
