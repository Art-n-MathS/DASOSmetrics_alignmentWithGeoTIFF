## package main
#  @brief this script is used for co-registering maps created using LiDAR data from DASOS with Sentinel2 Images
#
#  @details How to run the program: 
#  @details python main.py -inAsc <inputFolderWithAscs> -inGeoTif <inputGeoTifImage> -out <outFolder> 
#  @notes the first band of the inputGeoTifImage is used in the interpretation. Other QGIS software could be used to extract the bands of interest

#
#  @details Examples: IR:  python "C:/Users/milto/Documents/TEPAK/Marie_Curie_IF/Work Packages/WP5/Script for fusion/main.py" -inAsc "C:\Users\milto\Documents\TEPAK\Marie_Curie_IF\Work Packages\WP5\height_fullFlights" -inGeoTif "C:/Users/milto/Documents/TEPAK/Marie_Curie_IF/Work Packages/WP5/S2B_MSIL2A_20190406T002059_N0211_R116_T55HBA_20190406T020644.SAFE/T55HBA_20190406T002059_B08_10m.jp2.tif" -out "C:/Users/milto/Documents/TEPAK/Marie_Curie_IF/Work Packages/WP5/NIR_fullFlights"


#  @details Examples: Red:  python "C:/Users/milto/Documents/TEPAK/Marie_Curie_IF/Work Packages/WP5/Script for fusion/main.py" -inAsc "C:\Users\milto\Documents\TEPAK\Marie_Curie_IF\Work Packages\WP5\height_fullFlights" -inGeoTif "C:/Users/milto/Documents/TEPAK/Marie_Curie_IF/Work Packages\WP5/S2B_MSIL2A_20190406T002059_N0211_R116_T55HBA_20190406T020644.SAFE/T55HBA_20190406T002059_B04_10m.jp2.tif" -out "C:/Users/milto/Documents/TEPAK/Marie_Curie_IF/Work Packages/WP5/RED_fullFlights"

#



#
#  @author Dr. Milto Miltiadou
#  @date 30th Aug 2019
#  @version 1.0

import numpy as np
import argparse
import sys
import os
from osgeo import gdal
from gdalconst import *
import numpy as np
import glob
from osgeo import ogr
import csv
import re
import GeoImage
import subprocess


#  @details python main.py -inAsc <inputFolderWithAscs> -inGeoTif <inputGeoTifImage> -out <outFolder> 
#  @notes the first band of the inputGeoTifImage is used in the interpretation. Other QGIS software could be used to extract the bands of interest

# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-inAsc",
     required=True,
     help="path to folder containing the .asc height/DEM maps exported from DASOS",
     metavar='<string>')
parser.add_argument("-inGeoTif",
     required=True,
     help="path of the GeoTif image that has the same coordinate system as the DEM/height maps exported from DASOS",
     metavar='<string>')
parser.add_argument("-out",
     required=True,
     help="path direction of folder where the co-registered maps will be saved",
     metavar='<string>')




params    = vars(parser.parse_args())
inAsc     = params["inAsc"   ]
inGeoTif  = params["inGeoTif"]
outFolder = params["out"     ]

if outFolder[-1:]!='/':
   outFolder=outFolder+"/"
if inAsc[-1:]!='/':
   inAsc=inAsc+"/"

print "inAsc     = ", inAsc
print "inGeoTif  = ", inGeoTif 
print "outFolder = ", outFolder
if not os.path.exists(outFolder):
    os.makedirs(outFolder)

geoImg = GeoImage.GeoImage(inGeoTif)

files = [f for f in glob.glob(inAsc + "*.asc")]

# initialisation of variables 
ncols = 125
nrows = 126
xllcorner = 263477.19
yllcorner = 6034159
cellsize = 0.8
NODATA_value = -0

for f in files:
    head, tail = os.path.split(f)
    inFile = open(f,"r")
    countLine = 0
    outFileName = outFolder + tail + "RED.asc" 
    outFile = open(outFileName,"w")
    for line in inFile:
       countLine=countLine+1
       if(countLine<=6):
          outFile.write(line)
       if(countLine==1):
          ncols = int(line.split()[1])
       if(countLine==2):
          nrows = int(line.split()[1])
       if(countLine==3):
          xllcorner = float(line.split()[1])
       if(countLine==4):
          yllcorner = float(line.split()[1])
       if(countLine==5):
          cellsize = float(line.split()[1])
       if(countLine==6):
          NODATA_value = float(line.split()[1])
       # of the centre of the top left cell
       xtl = xllcorner + cellsize/2.0
       ytl = yllcorner + cellsize*nrows - cellsize/2.0
    for c in range(nrows):
       yc = ytl - cellsize*float(c)
       strLine = ""
       for r in range(ncols):
          xr = xtl + cellsize*float(r)
          value = geoImg.getPixelValue(xr,yc)
          if (value == None or value <0.0 or value >1.7E308):
             value = NODATA_value
          strLine = strLine + " " + str(value)
       outFile.write(strLine)
    outFile.close()
          
    print ""
    print f
    print ncols 
    print nrows
    print xllcorner 
    print yllcorner 
    print cellsize 
    print NODATA_value
 
print "   ***   EXIT   ***\n"





