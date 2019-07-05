# **Repository to support Allen Coral Atlas (ACA)**

This repository contain code to process [ACA](https://allencoralatlas.org/) planet data.

The scripts above were developed to build mosaics from Planet quads delivered in the Vulcan bucket. They are bassically python wrappers 
for [gdal tools](https://gdal.org/) and meant to be run in a linux environment (High Performance 
computer or a virtual machines in cloud computing platforms (e.g. [Google Cloud](https://cloud.google.com/)))



| Script        | Purpose           |
|:------------- |:-------------|  
|mosaic_depth.py|Build mosaic from depth and bottom reflectance| 
|mosaic_surfaceReflectance.py|Build mosaic from surface reflectance quads|  
|gdalcalcstats.py|Calculate stats and pyramids efficiently for big raster|

#### <i class="icon-file"></i> Create a document