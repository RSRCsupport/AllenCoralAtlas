#! /usr/bin/env python

"""
Problem: To mosaic planet surface reflectance (sr) quads for operational purposes in the Allen Coral Atlas. This script takes as arguments: 
1) an optional shapefile for including quads that need to be mosaicked. For example you may want to mask areas of no interest or  want 
to mosaic areas for which you have field data, then you use a shapefile and get quads mosaicked within that shapefile. For the Fiji mosaic this is key as mosaics are produced
using shapefiles to deal with datelines issues and the size of the mosaics to be ingested in Google earth engine (i.e. < 10GB)  
2) output data type per band (default UInt16 but can be set to any of these options Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/CInt16/CInt32/CFloat32/CFloat64) 
User: global coral project
Target system: Python (https://www.python.org/)
interface: PyCharm
Functional requirements:
                        inputs: A txt file with a list of planet quads (either depth or surface reflectance ones) and optional flags in 1) and 2) above 
                        outputs: A mosaic from quads listed in the txt file and spatially subset if the shapefile flag is included.
						
Examples: 
                    1) Displaying the script help (use the -h flag):
					
					Local/path/where/data/and/scripts/are > python mosaic_surfaceReflectance.py -h
					
					usage: mosaic_surfaceReflectance.py [-h] [-inputshp INPUTSHP] [-outputDataType OUTPUTDATATYPE]
                   inputTxtFile

This script mosaics planet depth or bottom reflectance quads with the options
1) to limit the output to a shapefile extent and 2) set datatype per bands
(see options below)

positional arguments:
  inputTxtFile          txt file built by ls *.tif > nameOfTheMosaic.txt with
                        the Planet depth or bottom reflectance quads to be
                        mosaicked

optional arguments:
  -h, --help            show this help message and exit
  -inputshp INPUTSHP    an optional shapefile for including quads that need to
                        be mosaicked 
  -outputDataType OUTPUTDATATYPE
                        output data type per band (default UInt16 but can be
                        set to any of these options Byte/Int16/UInt16/UInt32/I
                        nt32/Float32/Float64/CInt16/CInt32/CFloat32/CFloat64)(
                        default=UInt16)

					2) create a mosaic from a list of rasters in the text file "srMosaic.txt" (in the linux terminal 
					by doing ls *.tif > depthMosaic.txt), using a shapefile (srSubset.shp) and 
					setting Float32 as the final data type. IMPORTANT: the name of the .txt file that contains
					the list of rasters will be the final name for the mosaic. In this example "srMosaic.tif"
					
					Local/path/where/data/and/scripts/are > python mosaic_surfaceReflectance.py srMosaic.txt -inputshapefile srSubset.shp -outputDataType Float32
					
					
Author: Rodney Borrego Acevedo (r.borregoacevedo@uq.edu.au/rodbio2008@gmail.com) 4/07/2019)

"""
from __future__ import print_function
import argparse
import os
import sys

def makeVrt(infile):
    """
    make a virtual mosaic
    :param infile: txt listing all quads in a set location
    :return: a virtual mosaic
    """
    outname = infile[:-4] + ".vrt"
    cmd = 'gdalbuildvrt -input_file_list {} {}'.format(infile, outname)
    os.system(cmd)
    return (outname)


def subsetVrt(shp, infile):
    """
    Subsetting the virtual mosaic to be used as a mask 
    :param shp: a mask shapefile for the extent of the mosaic that will be built
    :param infile: the virtual mosaic from makeVrt function
    :return: a subset from the virtual mosaic
    """
    outname1 = "cut" + infile[:-4] + '.vrt'
    cmd = 'gdalwarp -of GTiff -dstnodata -999 -cutline {} -crop_to_cutline -dstalpha  {} {}'.format(shp, infile, outname1)
    os.system(cmd)
    return (outname1)


def makeMosaic(dataType,infile):
    """
    make the actual mosaic limited to the shp extent
    :param infile: subsetted vrt
    :return: the actual .tif mosaic
    """
    if infile.startswith('cut'):
	    outname2 = infile[3:-4] + '.tif'
    else:
	    outname2 = infile[:-4] + '.tif'
    cmd = "gdal_translate -of 'GTiff' -co COMPRESS=LZW -b 1 -b 2 -b 3 -b 4 -ot {} -co NUM_THREADS=ALL_CPUS -co BIGTIFF=YES --config GDAL_CACHEMAX 80000 {} {}".format(dataType,infile, outname2)
    os.system(cmd)
    return (outname2)


def stats(infile):
    """
    RIOS code to calc stats and pyramid efficiently
    :param infile: the .tif s mosaic
    :return: the .tif mosaic with stats and pyramids calculated
    """
    cmd = 'python gdalcalcstats.py {} -pyramid -ignore 0'.format(infile)
    os.system(cmd)

def getCmdargs():
    """
    Get command line args
    :return: options to set as a flags in script
    """
    parser = argparse.ArgumentParser(description='This script mosaics planet surface reflectance quads with the options 1) to limit the output to a shapefile extent and 2) set datatype per bands (see options below)')
    parser.add_argument('inputTxtFile', help='txt file built by ls *.tif > nameOfTheMosaic.txt with the Planet surface reflectance quads to be mosaicked')
    parser.add_argument('-inputshp', help='an optional shapefile for including quads that need to be mosaicked')
    parser.add_argument('-outputDataType', default = 'UInt16', type=str, help='output data type per band (default UInt16 but can be set to any of these options \
                      Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/CInt16/CInt32/CFloat32/CFloat64)(default=%(default)s)')
    cmdargs=parser.parse_args()
    
    if cmdargs.inputTxtFile is None:
        parser.print_help()
        sys.exit()
    return cmdargs

def mainRoutine():
    """
    main routine where everything happens
    :return: intermediate and final products
    """
    cmdargs = getCmdargs()
    print('building the virtual mosaic from {}....'.format(cmdargs.inputTxtFile))
    outname = makeVrt(cmdargs.inputTxtFile)
    print('subsetting the virtual mosaic {}.... '.format(outname))
	
    if cmdargs.inputshp:
        outname1 = subsetVrt(cmdargs.inputshp, outname)
        print('building mosaic {}'.format(outname1))
        outname2 = makeMosaic(cmdargs.outputDataType, outname1)
        os.remove(outname1)
    else:
        print('building mosaic {}'.format(outname))
        outname2 = makeMosaic(cmdargs.outputDataType, outname)
    print("Calculating stats from the mosaic {}....".format(outname2))
    stats(outname2)
	
    os.remove(outname)
    
if __name__ == "__main__":
    mainRoutine()


