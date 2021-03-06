# **Repository to support Allen Coral Atlas (ACA)**

This repository contain code to process [ACA](https://allencoralatlas.org/) planet data.

The python scripts above were developed to build mosaics from Planet quads delivered in the Vulcan bucket. They are basically python wrappers 
for [gdal tools](https://gdal.org/) and meant to be run in a Linux environment (High Performance 
computer (HPC) or virtual machines in cloud computing platforms (e.g. [Google Cloud](https://cloud.google.com/)))

Table 1. Scripts to mosaic Planet quads

| Script        | Purpose           |
|:------------- |:-------------|  
|mosaic_depth.py|Build mosaic from depth and bottom reflectance quads| 
|mosaic_surfaceReflectance.py|Build mosaic from surface reflectance quads|  
|gdalcalcstats.py|Calculate stats and pyramids efficiently for big raster|

### **How to set a virtual machine (VM) in Google Cloud Platform and install required python libraries**

Assuming that you've got an account in the Google Cloud Platform 
(if not follow [this](https://cloud.google.com/billing/docs/how-to/manage-billing-account))
and you created a project (if not follow
 [this](https://cloud.google.com/resource-manager/docs/creating-managing-projects)), next step 
 is to create a google cloud instance (i.e. Linux virtual machine) 
 ([see details here](https://cloud.google.com/compute/docs/quickstart-linux) and 
 [here](https://cloud.google.com/compute/docs/instances/create-start-instance)). For a more general documentation
 about virtual machines (see [this](https://cloud.google.com/compute/docs/instances/)). Figure below
 show a summarized sequence from creating to starting a VM.
 
 
 ![FlowchartVM](https://github.com/RSRCsupport/AllenCoralAtlas/blob/master/FlowChartVM.png)
 
 
 Due to the amount of data to be mosaicked and my experience using the HPC for running the codes, 
 the VM should have minimum 64 vCPU, 240 GB memory but the higher computer power
 the better, be of course mindful to turn off your VM when not in use to avoid being 
 extra charged :sob:. Storage may also be needed within the VM if data needs to be moved from the 
 Vulcan bucket to the VM's home directory (1 TB can be enough for Fiji data for example). You can use [Cloud 
 Storage FUSE](https://cloud.google.com/storage/docs/gcs-fuse) to mount google cloud buckets into the VM as well, however
 this system has much higher latency than working within the VM and can make your scripts slower. 
 
 Once the VM is started you will see a Linux terminal like the one below. 

 ![VMTerminal](https://github.com/RSRCsupport/AllenCoralAtlas/blob/master/VMlinuxterm.png)
 
 In the terminal type these lines of code one by one to install [miniconda](https://conda.io/en/latest/miniconda.html) 
 (compacted [Anaconda](https://www.anaconda.com/) version) that enables to easily install 
 libraries needed for the scripts to work.
 
 ````
 ~$ sudo apt-get update
 ~$ sudo apt-get install bzip2 libxml2-dev
 ~$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
 ````
 
 The shell script (.sh) for miniconda should be in the VM home directory, 
 just type the code below to have it installed. If you get permission errors, type `chmod 750 Miniconda3-latest-Linux-x86_64.sh`
 
 ````
 ~$ bash Miniconda3-latest-Linux-x86_64.sh
 ````
  Once miniconda is installed libraries like gdal or [rios](http://www.rioshome.org/en/latest/) can be installed via
  typical anaconda's "conda install" command line. To install gdal, for example, search in google "conda install gdal" 
  and you will get [this](https://anaconda.org/conda-forge/gdal), thus proceed with the line of code below. 
  
  ```` 
 ~$ conda install -c conda-forge gdal
  ````
 
 Same process with rios or any other libraries that need to be installed.
 
 
 ### **How to run the scripts in the virtual machine (VM) to build the mosaics**
 
 By default [gcloud SDK](https://cloud.google.com/sdk/docs/quickstart-linux) is included when you create your VM
 so you can use [gsutils](https://cloud.google.com/storage/docs/gsutil) to move data or scripts from the bucket/your pc
 to the VM's home directory. For example use the code below to move data from the Vulcan bucket to the VM's home dir
 
 First initialize the gcloud SDK and follow the prompts
 ````
 ~$ gcloud init
 ````
 Then use gsutil to move data
 
 ````
~$ gsutil -m cp -r gs://coral-atlas-data-pipeline/fiji_high_tide_normalized_sr_v2_aug2017_thru_april2019_mosaic-coastal-1 ~/
 
 ````
 
 The same process can be used to move all the scripts in Table 1 above to the VM's home dir
 
 Once all the scripts and data are available in the VM's home dir they can be run directly from the command line. 
 I included a help flag when I wrote the scripts. By using "-h" you will get a list with all the options available to pre-process data.
 A more detailed help with examples was included as docstrings in each code to better understand outputs you get from them.
 Below each script with their associated help. 
 
 - mosaic_depth.py
 ``````  
~$ python mosaic_depth.py -h
usage: mosaic_depth.py [-h] [-inputshp INPUTSHP]
                       [-outputDataType OUTPUTDATATYPE]
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

 ``````
 
 - mosaic_surfaceReflectance.py
 ````
~$ python mosaic_surfaceReflectance.py -h
usage: mosaic_surfaceReflectance.py [-h] [-inputshp INPUTSHP]
                                    [-outputDataType OUTPUTDATATYPE]
                                    inputTxtFile

This script mosaics planet surface reflectance quads with the options 1) to
limit the output to a shapefile extent and 2) set datatype per bands (see
options below)

positional arguments:
  inputTxtFile          txt file built by ls *.tif > nameOfTheMosaic.txt with
                        the Planet surface reflectance quads to be mosaicked

optional arguments:
  -h, --help            show this help message and exit
  -inputshp INPUTSHP    an optional shapefile for including quads that need to
                        be mosaicked
  -outputDataType OUTPUTDATATYPE
                        output data type per band (default UInt16 but can be
                        set to any of these options Byte/Int16/UInt16/UInt32/I
                        nt32/Float32/Float64/CInt16/CInt32/CFloat32/CFloat64)(
                        default=UInt16)
````
- gdalcalstats.py
````
~$ python gdalcalcstats.py -h
usage: gdalcalcstats.py [-h] [-pyramid] [-ignore IGNORE] imagefile

To neatly calculate stats (very efficiently) for big tif data. It uses the
RIOS packages available in anaconda at https://anaconda.org/conda-forge/rios

positional arguments:
  imagefile       Image file on which to calculate stats

optional arguments:
  -h, --help      show this help message and exit
  -pyramid        Calculate pyramid layers
  -ignore IGNORE  Stats ignore value (default is None)
````