# TRISO Fuel rod in OpenMC

Code builds a nested dictionary of the material data loaded from hdf5 files, creates the materials with the associated cross section data, assembles a graphite matrix fuel rod seeded with enriched TRISO pebbles, and outputs a cross section image.  

## XY cross section
![image](https://github.com/user-attachments/assets/7bedf978-0ec5-4d46-8bce-90d3fb225f6e)

## XZ cross section
![image](https://github.com/user-attachments/assets/0787dccc-fcfd-46a5-82e9-1ffb79bf69c0)




## TRISO fuel pebble specifications:

https://www.researchgate.net/publication/349432844_Analysis_of_water_ingress_accident_in_the_RDE_core_using_MCNPX

ID: 1, Kernel: UO2      , density[g/cm^3] = 10.41, radius[cm] = 0.0250   
ID: 2, Buffer: C12/13   , density[g/cm^3] = 01.14, radius[cm] = 0.0340\
ID: 3, IpyC  : C12/13   , density[g/cm^3] = 01.89, radius[cm] = 0.0380\
ID: 4, SiC   : SiC      , density[g/cm^3] = 03.20, radius[cm] = 0.0415\
ID: 5, OpyC  : C12/13   , density[g/cm^3] = 01.87, radius[cm] = 0.0455




## Fuel Rod Specifications 
* Enrichment set to 17%
* Packing fraction set to 0.3 


## Running this code in your environment
This code runs in the openmc conda-forge channel given the following dependencies:

* h5py==3.13.0
* numpy==2.3.1
* openmc==0.15.2

This repository uses Git LFS for the HDF5 files, so to run yourself:

    git lfs clone https://github.com/DOWingard/TRISO_Fuel_Rod
    cd TRISO_Fuel_Rod
    pip install -r requirments.txt
    python3 TRISO_Script.py
