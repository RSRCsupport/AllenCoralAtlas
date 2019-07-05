#!/usr/bin/env python
"""

Problem: To neatly calculate stats (very efficiently) for big tif data. It uses the RIOS packages available in anaconda at https://anaconda.org/conda-forge/rios
This script takes as arguments: 
1) -pyramid: to build pyramyd 
2) -ignore: to ignore specific values during stat calculation (e.g. 0 values)
Target system: Python (https://www.python.org/)
interface: PyCharm
Functional requirements:
                        inputs: A raster mosaic file (or a single image) and the optional flags as above
                        outputs: A raster mosaic file with stats calculated 
						
Examples: 
                    1) Displaying the script help:
					
				    Local/path/where/data/and/scripts/are >  python gdalcalcstats.py -h
					
usage: gdalcalcstats.py [-h] [-pyramid] [-ignore IGNORE] imagefile

positional arguments:
  imagefile       Image file on which to calculate stats

optional arguments:
  -h, --help      show this help message and exit
  -pyramid        Calculate pyramid layers
  -ignore IGNORE  Stats ignore value (default is None)


Maintainer: script developed by Neil Flood, just slightly modified by Rodney Borrego Acevedo (r.borregoacevedo@uq.edu.au/rodbio2008@gmail.com) 4/07/2019)

"""
from __future__ import print_function 

import argparse

from osgeo import gdal

from rios import calcstats, cuiprogress

def getCmdargs():
    """
    Get commandline arguments. These are deigned to be
    backwards compatible with the old C++ code, but more options
    could be added if required. 
    
    """
    p = argparse.ArgumentParser()
    p.add_argument("imagefile", help="Image file on which to calculate stats")
    p.add_argument("-pyramid", default=False, action="store_true",
        help="Calculate pyramid layers")
    p.add_argument("-ignore", type=float, help="Stats ignore value (default is None)")
    return p.parse_args()


def mainRoutine():
    cmdargs = getCmdargs()
    
    # First set the ignore value into the file
    ds = gdal.Open(cmdargs.imagefile, gdal.GA_Update)
    if cmdargs.ignore is not None:
        for i in range(ds.RasterCount):
            band = ds.GetRasterBand(i+1)
            band.SetNoDataValue(cmdargs.ignore)
    del ds
    
    ds = gdal.Open(cmdargs.imagefile, gdal.GA_Update)

    progress = cuiprogress.SilentProgress()
    
    calcstats.addStatistics(ds, progress, cmdargs.ignore)
    
    if cmdargs.pyramid:
        calcstats.addPyramid(ds, progress)
        
    del ds


if __name__ == "__main__":
    mainRoutine()

