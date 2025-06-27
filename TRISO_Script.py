from TRISO_tools.TRISO import data_loader, Compacts


##########################################################################################
'''
Main script that performs the main functions specified in TRISO_tools:

* Loads data from .h5 files into nested dict and initializes experimental parameters
* Assembles a TRISO fuel rod from the material data (outputs xml files [geometry, materials, plots])
* Creates cross section plot  

D. Wingard 6/2025
'''
##########################################################################################



data_folder = './Data'
model_path  = './Model_Files'
h5file_path = './Data/Neutron'
import_path = './Model_Files'
export_path = import_path
materials_file = './Model_Files/materials.xml'



enrichment_amount = 0.17
packing_fraction=0.30


Simulation_data = data_loader(h5file_path)
TRISO_fuel_rod = Compacts(h5file_path,export_path,enrichment_amount)
TRISO_fuel_rod.build_fuel_rod(materials_file,export_path,packing_fraction)




# Plot parameters

width = (1.6,1.6)
pixels = (1000,1000)
origin =(0.0,0.0,0.0)
basis = 'xy'


# images output to the CWD (Model_Files folder at export/import_path)
TRISO_fuel_rod.plot_xs(
    export_path, 
    width, 
    pixels, 
    origin, 
    basis 
    )