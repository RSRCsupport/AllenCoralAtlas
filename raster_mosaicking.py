#! /usr/bin/env python

"""
Problem: To mosaic any raster efficiently, specifically if they are big
User: global coral project
Target system: Python (https://www.python.org/)
interface: PyCharm
Functional requirements:
                        ##inputs: A txt file with a list of rasters
                        ##outputs: A mosaic 

Author: Rodney Borrego Acevedo (r.borregoacevedo@uq.edu.au, 2/05/2019)

"""
from __future__ import print_function
import argparse
import os


def makeVrt(infile):
    """
    make a virtual mosaic
    :param infile: txt listing all surface reflectance tiles in a set location
    :return: a virtual mosaic
    """
    outname = infile[:-4] + ".vrt"
    cmd = 'gdalbuildvrt -input_file_list {} {}'.format(infile, outname)
    os.system(cmd)
    return (outname)


def makeMosaic(infile):
    """
    make the actual surface reflectance mosaic limited to the shp extent using 24 cores and 80 GB memory in the High Performance Computer
    :param infile: subsetted vrt
    :return: the actual .tif surface reflectance mosaic
	Note: output to LZW compression and byte to reduce size
    """
    outname1 = infile[:-4] + '.tif'
    cmd = "gdal_translate -of 'GTiff' -b 1 -b 2 -b 3  -co COMPRESS=LZW -co NUM_THREADS=ALL_CPUS -co BIGTIFF=YES --config GDAL_CACHEMAX 80000 {} {}".format(infile, outname1)
    os.system(cmd)
    return (outname1)


def stats(infile):
    """
    RIOS code to calc stats and pyramid efficiently easy to use
    :param infile: the .tif surface reflectance mosaic
    :return: the .tif surface reflectance mosaic with stats calculated
    """
    cmd = 'python gdalcalcstats.py {} -pyramid -ignore 0'.format(infile)
    os.system(cmd)


def getCmdargs():
    """
    Get command line args
    :return: options to set as a flags in script
    """
    parser = argparse.ArgumentParser(description='this script mosaic raster data efficiently')
    parser.add_argument('-inputtxt', '--filelist', help='txt file with the images to be mosaicked')
    
    return parser.parse_args()


def mainRoutine():
    """
    main routine where everything happens
    :return: intermediate and final products
    """
    cmdargs = getCmdargs()
    print('building the virtual mosaic from {}....'.format(cmdargs.filelist))
    outname = makeVrt(cmdargs.filelist)
    print('building mosaic {}'.format(outname))
    outname1 = makeMosaic(outname)
    print("Calculating stats from the mosaic {}....".format(outname1))
    stats(outname1)


if __name__ == "__main__":
    mainRoutine()


