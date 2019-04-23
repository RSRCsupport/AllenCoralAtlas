#! /usr/bin/env python

"""
Problem: To mosaic planet quads for areas where field data exist as a way to reduce the size of mosaics used for operational purposes
User: global coral project
Target system: Python (https://www.python.org/)
interface: PyCharm
Functional requirements:
                        ##inputs: A txt file with a list of planet quads
                        ##outputs: A mosaic for areas where field data is available (.shp)

Author: Rodney Borrego Acevedo (r.borregoacevedo@uq.edu.au)

"""
from __future__ import print_function
import argparse
import os


def makeVrt(infile):
    """
    make a virtual mosaic
    :param infile: txt listing all tiles in a set location
    :return: a virtual mosaic
    """
    outname = infile[:-4] + ".vrt"
    cmd = 'gdalbuildvrt -input_file_list {} {}'.format(infile, outname)
    os.system(cmd)
    return (outname)


def subsetVrt(shp, infile):
    """
    Subsetting the virtual mosaic,the combination between dstnodata and dstalpha make the 9999 trasnparent
    :param shp: a mask shapefile for the extent the mosaci will be built
    :param infile: the virtual mosaic from makeVrt function
    :return: a subset from the virtual mosaic
    """
    outname1 = "cut" + infile[:-4] + '.vrt'
    cmd = 'gdalwarp -of GTiff -dstnodata -9999 -cutline {} -crop_to_cutline -dstalpha  {} {}'.format(shp, infile, outname1)
    os.system(cmd)
    return (outname1)


def makeMosaic(infile):
    """
    make the actual mosaic limited to the shp extent using 24 cores and 80 GB memory in the High Performance Computer
    :param infile: subsetted vrt
    :return: the actual .tif mosaic
    """
    outname2 = infile[3:-4] + '.tif'
    cmd = "gdal_translate -of 'GTiff' -b 1 -co NUM_THREADS=ALL_CPUS -co BIGTIFF=IF_NEEDED --config GDAL_CACHEMAX 80000 {} {}".format(
        infile, outname2)
    os.system(cmd)
    return (outname2)


def stats(infile):
    """
    RIOS code to calc stats and pyramid efficiently
    :param infile: the .tif mosaic
    :return: the .tif mosaic with stats calculated
    """
    cmd = 'python gdalcalcstats.py {} -pyramid '.format(infile)
    os.system(cmd)


def adjustDepth(infile):
    """
    this is to bring data to m
    :param infile: the .tif mosaic (-1 to 1500)
    :return: the .tif mosaic (-0.01 to 15 m)
    """
    outname3 = infile[:-4] + '_FieldData' + '.tif'
    cmd = "gdal_calc.py -A {} --A_band=1 --NoDataValue=0 --format 'GTiff' --outfile={} --type=Float32 --calc='(A/100.00)'".format(
        infile, outname3)
    os.system(cmd)
    return (outname3)


def getCmdargs():
    """
    Get command line args
    :return: options to set as a flags in script
    """
    parser = argparse.ArgumentParser(description='this script mosaic planet quads included in a mask shapefile')
    parser.add_argument('-inputtxt', '--filelist', help='txt file with the images to be mosaicked')
    parser.add_argument('-inputshp', '--shapefile', help='shapefile with the field data mask')
    return parser.parse_args()


def mainRoutine():
    """
    main routine where everything happens
    :return: intermediate and final products
    """
    cmdargs = getCmdargs()
    print('building the virtual mosaic from {}....'.format(cmdargs.filelist))
    outname = makeVrt(cmdargs.filelist)
    print('subsetting the virtual mosaic {}.... '.format(outname))
    outname1 = subsetVrt(cmdargs.shapefile, outname)
    print('building mosaic {}'.format(outname1))
    outname2 = makeMosaic(outname1)
    print("Calculating stats from the mosaic {}....".format(outname2))
    stats(outname2)


# print ("Adjusting depth values for {}".format(outname2))
# outname3=adjustDepth(outname2)
# print ("Finally calculating stats from {}....".format(outname3))
# stats(outname3)

if __name__ == "__main__":
    mainRoutine()


