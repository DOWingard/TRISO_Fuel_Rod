import openmc
import openmc.data
import numpy as np
import h5py
import os
from dataclasses import dataclass

##########################################################################################
'''
Simple code that creates a few classes:

data_loader : loads and data from .h5 files so that it may be easily accessed and stores experimental parameters
Compacts    : constructs TRISO-in-graphite fuel rod (openmc.Universe) and a materials list (openmc.Materials)

D. Wingard 6/2025
'''
##########################################################################################


endf_path   = '/home/derek/Downloads/E4R83298_e4.txt'  
ace_path    = '/home/derek/Downloads/ENDF-B-VII.1-tsl/graphite.acer'
model_path  = '/home/derek/Desktop/TRISO_Project/Model_Files'
data_folder = '/home/derek/Desktop/TRISO_Project/Data'


##########################################################################################
'''
data loader 
'''
##########################################################################################


@dataclass
class data_loader:
    '''
    
    Stores experimental parameters
    Loads data from .h5 files into a similarly structured nested dictionary. 
    Conversion of data to h5 was ignored as data was sourced from multiple filetypes.
    
    Args:
            path (str): path to folder containing subfolders with .h5 files
        
    '''

    
    def __init__(self,path):
        
        self.filepath = path
        self.data = {}
        self.isotopes = ['U235', 'U238','O16','C12','C13','Si28']
        self.temperatures_n = [0, 1200, 2500, 250, 294, 600, 900]
        self.tempkeys_n =  ['0K', '1200K', '2500K', '250K', '294K', '600K', '900K']
        self.temperatures_grph = [296]
        self.tempkeys_grph = ['296K']
        
        
        
    def load_data(self,path):
        """
        Loads data into a nested dict which respects file structure

        Args:
            path (str): path to folder containig subfolders with .h5 files
        """
        
        the_data = {}
        for folder in os.listdir(path):
            path2 = os.path.join(path,folder)
            for h5file in os.listdir(path2):
                nested_dict = self._update_dataset(os.path.join(path2,h5file))
                the_data[h5file] = nested_dict
        self.data = self._clip_top_layer(the_data)
    
    
                    
    def _update_dataset(self,path):
        """
        Assigns initial empty dict to each file
        Args:
            path (str): path to folder containig subfolders with .h5 files

        Returns:
            Nested dict: nested dictionary containing the data
        """
        h5file = h5py.File(path,'r')
        return self._assign_dataset({},h5file)
        
    
            
    def _assign_dataset(self,data_structure,dct):
        
        return self._build_dataset(data_structure, dct)
        
    
    
    def _build_dataset(self,data_structure,dct,key=None):
        
        for key in dct.keys():

            if isinstance(dct[key],h5py.Group):
                data_structure[key] = {}
                self._build_dataset(data_structure[key],dct[key],key)
                
            if isinstance(dct[key],h5py.Dataset):
                data_structure[key] = dct[key]

                
            
        return   data_structure     



    def _clip_top_layer(self,dct):
        """
        Begins dictionary nesting at layer 1 instead of 0 because they repeat
        """
        new_and_improved_dict = {}
        
        for key in dct.keys():
            strkey = key[:-3]
            
            new_and_improved_dict[strkey] = dct[key][strkey]
        
        return new_and_improved_dict
    



##########################################################################################
'''
Compacts 
'''
##########################################################################################


@dataclass 
class Compacts:
    """
    Constructs an openmc.Universe object for a TRISO fuel rod and an array of openmc.Materials with the correct cross section data 
    
    Args:
            path (str): path to folders
            
    Returns:
            TRISO rod (openmc.Universe) and array of materials [openmc.Material,...]        
    """
    
    
    
        
    def __init__(self,h5file_path,export_path, enrichment=0.17):
        openmc.reset_auto_ids()
        self._TRISO_materials(h5file_path,export_path, enrichment)
        
    
    
    
    def build_fuel_rod(self,import_path,export_path,packing_fraction):
    
        cmpctuniv, ctube, cbtm, ctop = self._construct_compacts(import_path,export_path,packing_fraction)
        return cmpctuniv, ctube, cbtm, ctop
    
    
    
    def _TRISO_materials(self,h5file_path, export_path, enrich=0.1700):
        
        """
        creates objects for materials in pebbles
        
        parameters found from ResearchGate: Analysis of water ingress accident in the RDE core using MCNPX
        
        
        nuclide densities and such found on openmc TRISO examples page
        Args:
            path (str): path to folders
        """
        
        
        openmc.config['cross_sections'] = h5file_path
        UO2_kernel = openmc.Material(name = 'UO2 Fuel Kernel')
        
        
        #Fuel Kernel 

        UO2_kernel.add_nuclide('U235', enrich * (1/3), 'ao')
        UO2_kernel.add_nuclide('U238', (1-enrich) * (1/3), 'ao')
        UO2_kernel.add_nuclide('O16', 2/3, 'ao')
        UO2_kernel.set_density('g/cm3',10.5000)             
        
        
        #Buffer 
        
        buffer = openmc.Material(name = 'Buffer')
        buffer.add_nuclide('C12', 1.0)
        buffer.set_density('g/cm3', 1.0000)
        buffer.add_s_alpha_beta('c_Graphite')
        
        
        # IpyC
        
        ipyc = openmc.Material(name = 'IpyC')
        ipyc.add_nuclide('C12', 1.0)
        ipyc.set_density('g/cm3', 1.9000)
        ipyc.add_s_alpha_beta('c_Graphite')
        
        
        #SiC
        
        sic = openmc.Material(name = 'SipyC')
        sic.add_nuclide('Si28',1.0)
        sic.add_nuclide('C12', 1.0)
        sic.set_density('g/cm3', 3.2000)
        
        
        #OpyC 
        
        opyc = openmc.Material(name = 'OpyC')
        opyc.add_nuclide('C12', 1.0)
        opyc.set_density('g/cm3',1.8700)
        opyc.add_s_alpha_beta('c_Graphite')
        
        
        #Graphite-lower density
        
        graphite = openmc.Material(name = 'Graphite')
        graphite.set_density('g/cm3', 1.1995)
        graphite.add_nuclide('C12', 1.0)
        graphite.add_s_alpha_beta('c_Graphite')
        
        
        #Graphite Matrix
        
        graphite_matrix = openmc.Material(name = 'Prismatic Graphite')
        graphite_matrix.add_nuclide('C12', 1.0)
        graphite_matrix.set_density('g/cm3', 1.7520)  #halfway between 2nd and 3rd reactor generations given in ScienceDirect paper
        graphite_matrix.add_s_alpha_beta('c_Graphite')
        
        
        #Graphite Moderator
        
        graphite_moderator= openmc.Material(name = 'Graphite moderator')
        graphite_moderator.add_nuclide('C12', 1.0)
        graphite_moderator.set_density('g/cm3', 2.0000)  
        graphite_moderator.add_s_alpha_beta('c_Graphite')
        
        
        #write out all materials
        
        materials = openmc.Materials([UO2_kernel, buffer, ipyc, sic, opyc, graphite, graphite_matrix, graphite_moderator])
        materials.export_to_xml(export_path)
        


    def _create_TRISO_pebble(self, import_path):
        
        """
        Constructs the fuel pebbles per specifications given at:
        
        ResearchGate: Analysis of water ingress accident in the RDE core using MCNPX
        
        ID: 1, Kernel: UO2      , density[g/cm^3] = 10.41, radius[cm] = 0.0250   -   17% U235, 83% U238
        ID: 2, Buffer: C12/13   , density[g/cm^3] = 01.14, radius[cm] = 0.0340
        ID: 3, IpyC  : C12/13   , density[g/cm^3] = 01.89, radius[cm] = 0.0380
        ID: 4, SiC   : SiC      , density[g/cm^3] = 03.20, radius[cm] = 0.0415
        ID: 5, OpyC  : C12/13   , density[g/cm^3] = 01.87, radius[cm] = 0.0455
        
        """
        
        materials = openmc.Materials.from_xml(import_path)  ### ID (array ref + 1): [1,2,3,4,5,6,7,8] -> [Kernel,Buffer,IpyC,SiC,OpyC,Graphite,Graphite Matrix,Graphite Moderator]
        
        rad_ker  = 0.0250   # [cm]
        rad_buff = 0.0340
        rad_ipyc = 0.0380
        rad_sic  = 0.0415
        rad_opyc = 0.0455
        
        
        #Construct the shells
        
        shell_ker  = openmc.Sphere(r=rad_ker )
        shell_buff = openmc.Sphere(r=rad_buff)
        shell_ipyc = openmc.Sphere(r=rad_ipyc)
        shell_sic  = openmc.Sphere(r=rad_sic )
        shell_opyc = openmc.Sphere(r=rad_opyc)
        
        
        #create the layers between each shell
        
        kernel_cell = openmc.Cell(fill = materials[0], region = -shell_ker               )
        buffer_cell = openmc.Cell(fill = materials[1], region = +shell_ker  & -shell_buff)
        ipyc_cell   = openmc.Cell(fill = materials[2], region = +shell_buff & -shell_ipyc)
        sic_cell    = openmc.Cell(fill = materials[3], region = +shell_ipyc & -shell_sic )
        opyc_cell   = openmc.Cell(fill = materials[4], region = +shell_sic  & -shell_opyc)
        
        
        #write out the TRISO pebble as a universe with its radius
        
        TRISO_univ = openmc.Universe(cells= [kernel_cell, buffer_cell, ipyc_cell, sic_cell, opyc_cell])
        
        return TRISO_univ, rad_opyc
        
        
        
        
    def _construct_compacts(self, 
                            import_path, 
                            export_path, 
                            radius = 0.7, 
                            height = 5, 
                            packing_fraction=0.30    # pf=0.30: safe number I guess...
                            ):  
        
        """
        constructs the actual fuel compact as an openmc.Universe object

        Returns:
            openmc.Universe : TRISO rod universe object
            openmc.ZCylinder: Radial boundary cylinder 
            openmc.Zplane   : Bottom boundary plane
            openmc.Zplane   : Top boundary plane
        """
        
        
        compact_rad = radius
        compact_height = height  
        
        
        
        #build the compact surfaces
        
        compact_tube = openmc.ZCylinder(r =  compact_rad)
        compact_btm  = openmc.ZPlane(  z0 = -compact_height/2)
        compact_top  = openmc.ZPlane(  z0 =  compact_height/2)
        compact_region = -compact_tube & +compact_btm & -compact_top
        
        
        TRISO_univ, pebble_radius = self._create_TRISO_pebble(import_path)
        materials = openmc.Materials.from_xml(import_path) ### ID (array ref + 1): [1,2,3,4,5,6,7,8] -> [Kernel,Buffer,IpyC,SiC,OpyC,Graphite,Graphite Matrix,Graphite Moderator]
        
        
        #generate origins^\dag for randomly packed spheres within the cylindrical region
        
        sphere_locations = openmc.model.pack_spheres(pebble_radius, compact_region, packing_fraction)
        
        
        
        #Initialize graphite matrix region and the main universe to represent the fuel compact
        
        graphite_matrix = compact_region
        compact_universe = openmc.Universe(name = 'fuel_compact')
        
        
        #for every origin^\dag, create a sphere
        #use that sphere to construct a cell filled with the TRISO universe
        #translates the cell accordingly to ensure locations of pebbles
        #adds each cell to the main universe
        # the initialized graphite matrix region is updated via intersection of itself with each region of -sphere, carving out the locations
        ###  ^^^potentially unnecessary as the ordering of geometry creation alone would suffice for the binary operation?
        
        for point in sphere_locations:
            
            x,y,z = point
            sphere = openmc.Sphere(x0=x,y0=y,z0=z,r=pebble_radius)
            TRISO_cell = openmc.Cell(fill=TRISO_univ, region=-sphere)
            TRISO_cell.translation = (x,y,z)
            compact_universe.add_cell(TRISO_cell)
            graphite_matrix = graphite_matrix & +sphere
        
        #write out everything as a geometry.xml file
        graphite_matrix_material_cell = openmc.Cell(fill = materials[6], region = graphite_matrix )
        compact_universe.add_cell(graphite_matrix_material_cell)
        geo = openmc.Geometry(compact_universe)
        geo.export_to_xml(export_path)
        
        
        return compact_universe, compact_tube, compact_btm, compact_top
    
    
    def plot_xs(self, 
                export_path, 
                width, 
                pixels, 
                origin, 
                basis
                ):
        '''
        Creates a plots.xml file then plots using openmc.plot_geometry()
        '''
        plot = openmc.Plot()
        plot.filename = f'{basis}-plane_at_{origin}.png'
        plot.type     = 'slice'
        plot.basis    = basis
        plot.origin   = origin
        plot.width    = width
        plot.pixels   = pixels
        plot.color_by = 'cell'
        
        plots = openmc.Plots([plot])
        plots.export_to_xml(export_path)
        
        cwd = os.getcwd()
        os.chdir(export_path)
        openmc.plot_geometry()
        os.chdir(cwd)
        
        
    
        
        
        