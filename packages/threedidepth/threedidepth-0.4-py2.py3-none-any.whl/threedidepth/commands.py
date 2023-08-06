# -*- coding: utf-8 -*-

import argparse
import sys

from osgeo import gdal

from threedidepth.calculate import calculate_waterdepth
from threedidepth.calculate import MODE_LIZARD
from threedidepth.calculate import MODE_CONSTANT


def threedidepth(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "gridadmin_path", metavar="gridadmin", help="path to gridadmin file"
    )
    parser.add_argument(
        "results_3di_path",
        metavar="results_3di",
        help="path to simulation results file",
    )
    parser.add_argument(
        "dem_path", metavar="dem", help="path to bathymetry file"
    )
    parser.add_argument(
        "waterdepth_path",
        metavar="waterdepth",
        help="path to resulting geotiff"
    )
    parser.add_argument(
        "-s",
        "--steps",
        nargs="+",
        type=int,
        default=[-1, ],
        dest="calculation_steps",
        help="simulation result step(s)",
    )
    parser.add_argument(
        "-c",
        "--constant",
        action="store_true",
        help="disable interpolation and use constant waterlevel per grid cell",
    )
    parser.add_argument(
        "-p",
        "--progress",
        action="store_const",
        dest="progress_func",
        const=gdal.TermProgress_nocb,
        help="Show progress.",
    )
    parser.add_argument(
        "-n",
        "--netcdf",
        action="store_true",
        help="export the waterdepth as a netcdf"
    )
    kwargs = vars(parser.parse_args())
    if kwargs.pop("constant"):
        kwargs["mode"] = MODE_CONSTANT
    else:
        kwargs["mode"] = MODE_LIZARD
    calculate_waterdepth(**kwargs)


if __name__ == '__main__':
    threedidepth(sys.argv)
