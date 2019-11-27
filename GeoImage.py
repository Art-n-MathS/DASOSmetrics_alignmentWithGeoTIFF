
## @package GeoImage2
#  This class contains an image and can apply various functions to it 
#  (for example canny edge).
#  @author Dr. Milto Miltiadou
#  @date Oct 2017 - Updated Aug 2019
#  @version 2.0


import numpy as np
import cv2
from osgeo import gdal
from gdalconst import *

## 
class GeoImage:


    ## The constructor
    #  @param i_inputTif the input image in tif format
    def __init__(self, i_inputTif):
        inp_raster = gdal.Open(i_inputTif)
        ## the value that represents null within the image
        self.noValue = inp_raster.GetRasterBand(1).GetNoDataValue()
        self.cols = inp_raster.RasterXSize
        self.rows = inp_raster.RasterYSize
        print self.noValue, self.cols, self.rows, "***************************"
        self.imArr = inp_raster.ReadAsArray(0,0,self.cols,self.rows)
        
        ## the geo transformation of the image
        self.geoTransform = inp_raster.GetGeoTransform()
        self.xOrigin     = self.geoTransform[0] 
        self.yOrigin     = self.geoTransform[3] 
        self.pixelWidth  = self.geoTransform[1] 
        self.pixelHeight = -self.geoTransform[5] 

        ## the projection of the image
        self.projection = inp_raster.GetProjection()

    ## method that takes as input a geolocation and returns the pixels value that it lies inside
    def getPixelValue(self, i_geoX, i_geoY): 
        xOffset = int((i_geoX - self.xOrigin) / self.pixelWidth)
        yOffset = int((self.yOrigin-i_geoY) / self.pixelHeight)
        if (xOffset>=0 and xOffset<self.cols and yOffset>0 and yOffset<self.rows):
           return self.imArr[yOffset][xOffset]
        else:
           return self.noValue

