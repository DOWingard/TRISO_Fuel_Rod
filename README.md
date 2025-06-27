# TRISO Fuel rod in OpenMC

Code builds a nested dictionary of the material data loaded from hdf5 files, creates the materials with the associated cross section data, assembles a graphite matrix fuel rod seeded with enriched TRISO pebbles, and outputs a cross section image.  

## TRISO fuel pebble specifications:

https://www.researchgate.net/publication/349432844_Analysis_of_water_ingress_accident_in_the_RDE_core_using_MCNPX

ID: 1, Kernel: UO2      , density[g/cm^3] = 10.41, radius[cm] = 0.0250   
ID: 2, Buffer: C12/13   , density[g/cm^3] = 01.14, radius[cm] = 0.0340
ID: 3, IpyC  : C12/13   , density[g/cm^3] = 01.89, radius[cm] = 0.0380
ID: 4, SiC   : SiC      , density[g/cm^3] = 03.20, radius[cm] = 0.0415
ID: 5, OpyC  : C12/13   , density[g/cm^3] = 01.87, radius[cm] = 0.0455




## Fuel Rod Specifications 
* Enrichment set to 17%
* Packing fraction set to 0.3 


## Running this code in your environment
This code runs in the openmc conda-forge channel given the following dependencies:

* h5py==3.13.0
* numpy==2.3.1
* openmc==0.15.2

Program allows for changes in parameters to the build so to run yourself:


    *in openmc-env*

* git clone https://github.com/DOWingard/TRISO_Fuel_Rod
* cd TRISO_Fuel_Rod
* pip install -r requirments.txt
* python3 TRISO_Script.py