"""

Project: FTIRDB
File: models/FTIRModel.py

Version: v1.0
Date: 10.09.2018
Function: Create the main tables in the BIRDB

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

This file contains the SQLalchemy model for the BIRDB (originally refered to as FTIRDB)

The model includes any contstraints that entered data should adhere to as well as any
links to other models.


"""

#import necessary modules from sqlalchemy

from sqlalchemy import (
    Column,
    Index,
    Integer,
    text,
    Text,
    ForeignKey,
    String,
    Float,
    CheckConstraint
    
)

from .meta import Base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Date, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

#immport colander lib 

import colander
from colander import Range
from sqlalchemy import Column, Date, Enum, ForeignKey, LargeBinary, String, Table
from sqlalchemy.dialects.mysql import INTEGER, LONGBLOB, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


metadata = Base.metadata


class project(Base):
    __tablename__ = 'project'

    descriptive_name = Column(String(500),info={'colanderalchemy': {'description': 'explain what the project is'}})
    project_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    related_experiments_ID = Column(String(100),info={'colanderalchemy': {'description': 'provide ID of any existing related experiments'}})
   

    
class sample(Base):
    __tablename__ = 'sample'

    sample_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    descriptive_name = Column(String(500))
    composition = Column(String(300), info={'colanderalchemy': {'description': 'Description of the composition'}})
    project_ID = Column(INTEGER(6),info={'colanderalchemy': {'exclude': True}})


class state_of_sample(Base):
    __tablename__ = 'state_of_sample'

    state_of_sample_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    state = Column(Enum('gas', 'solid', 'dried film', 'liquid',''), nullable=False, info={'colanderalchemy': {'exclude': True}})
    temperature_degrees = Column(INTEGER(11), default=0, info={'colanderalchemy': {'description': 'In degrees centigrade'}})
    pressure_PSI = Column(INTEGER(11), default=0, info={'colanderalchemy': {'validator': Range(min=0, max=1000), 'description': 'PSI'}})
    #child 
    sample_ID = Column(Integer, ForeignKey('sample.sample_ID'),  info={'colanderalchemy': {'exclude': True}})

class molecules_in_sample(Base):
    __tablename__ = 'molecules_in_sample'

    molecular_composition_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    descriptive_name = Column(String(300))
    molecule_1_name = Column(String(45))
    concentration_1 = Column(INTEGER(11) ,default = 100, info={'colanderalchemy': {'validator': Range(min=1, max=100),'description': 'as a %'}})
    molecule_2_name = Column(String(45))
    concentration_2 = Column(INTEGER(11),default = 100, info={'colanderalchemy': {'validator': Range(min=1, max=100),'description': 'as a %'}})
    molecule_3_name = Column(String(45))
    concentration_3 = Column(INTEGER(11), default = 100,info={'colanderalchemy': {'validator': Range(min=1, max=100),'description': 'as a %'}})
    molecule_4_name = Column(String(45))
    concentration_4 = Column(INTEGER(11),default = 100, info={'colanderalchemy': {'validator': Range(min=1, max=100),'description': 'as a %'}})

    #child
    sample_ID = Column(Integer,  info={'colanderalchemy': {'exclude': True}})




class liquid(Base):
    __tablename__ = 'liquid'

  
    pH = Column(Integer, default = 7, info={'colanderalchemy': {'validator': Range(min=0, max=14),'description': 'Between 0 and 14'}})
    solvent = Column(String(45), info={'colanderalchemy': {'description':'name of solvent'}})
    atmosphere = Column(String(45),info={'colanderalchemy': {'description': 'psi'}})
    liquid_ID =  Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})


    state_of_sample_ID = Column(Integer, info={'colanderalchemy': {'exclude': True}})




class dried_film(Base):
    __tablename__ = 'dried_film'

    atmosphere = Column(String(45),info={'colanderalchemy': {'description': 'kPa'}})
    volume = Column(String(45), info={'colanderalchemy': {'description': 'mm^3'}})
    area = Column(String(45),info={'colanderalchemy': {'description': 'mm^2'}})
    solvent = Column(String(45), info={'colanderalchemy': {'description': 'name of solvent'}})
    pH = Column(String(45), server_default=text("'RANGE(0,14)'"), info={'colanderalchemy': {'validator': Range(min=0, max=14),'description': 'Between 0 and 14'}})
    
    dried_film_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})


    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'), info={'colanderalchemy': {'exclude': True}})


class gas(Base):
    __tablename__ = 'gas'

    atmosphere = Column(String(45), info={'colanderalchemy': {'description': 'atmosphere in psi'}})
    water_vapour = Column(String(45), info={'colanderalchemy': {'description': 'g/m3'}})
    gasID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})

    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'), info={'colanderalchemy': {'exclude': True}})


class solid(Base):
    __tablename__ = 'solid'

    crystal_form = Column(String(45))
    chemical_formula = Column(String(45))
    solid_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})

    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'), info={'colanderalchemy': {'exclude': True}} )



class molecule(Base):
    __tablename__ = 'molecule'

    molecule_name = Column(String(45), nullable=False)
    molecule_ID = Column(INTEGER(11), primary_key=True, autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    #adding for now to associate with sample but ideally would use an association table
    sample_ID = Column(INTEGER(11), default=0, info={'colanderalchemy': {'exclude': True}})


#association table for relationship, not currently in use
association_molecule = Table(
    'association_molecule', metadata,
    Column('mols_in_sample_ID', ForeignKey('molecules_in_sample.molecular_composition_ID'), primary_key=True),
    Column('molecule_ID', ForeignKey('molecule.molecule_ID'), nullable=False, index=True)
)    
    
class protein(Base):
    __tablename__ = 'protein'
    sample_ID = Column(Integer, nullable=True, info={'colanderalchemy': {'exclude': True}})
    protein_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    protein_common_name = Column(String(300))
    alternative_names = Column(String(300))
    source_organism = Column(String(300))
    uniprot_ID = Column(String(300))
    sequence= Column('sequence', String(300), info={'colanderalchemy': {'description': 'Will get to autopoulate using biopython in future'}})
    expression_system_or_natural_source = Column(String(300))
    expressed_as = Column(String(300))
    post_translational_modifications = Column(String(300))
    mutation_details = Column(String(300))
    expression_tags = Column(String(300))
    isotopically_labelled = Column(Enum('yes', 'no',''), default = 'no')
    description_of_labels = Column(String(100), info={'colanderalchemy': {'description': 'if yes'}})
    ligands_present = Column(Enum('yes', 'no',''), default = 'no')

    #one to one relationshiip with molecule
    # 1 to 1 relationship
    molecule_ID = Column(Integer, nullable=True, info={'colanderalchemy': {'exclude': True}}) 


class chemical(Base):
    __tablename__ = 'chemical'

    chemical_ID =Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    CAS = Column(String(20), info={'colanderalchemy': {'description': 'write in the format xxxxxx-xx-x'}})
    smiles_inchi_mol2 = Column(String(300), info={'colanderalchemy': {'description':'smiles/inchi or mol2'}})
    chemical_formula = Column('chemical formula', String(300))
    molecule_ID = Column(Integer, nullable=True, info={'colanderalchemy': {'exclude': True}})

class other(Base):
    __tablename__ = 'other'

    other_ID =Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    name = Column(String(300))
    description = Column(String(300))
    molecule_ID = Column(Integer, nullable=True, info={'colanderalchemy': {'exclude': True}})

class experiment(Base):
    __tablename__ = 'experiment'

    experiment_ID =Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    name  = Column(String(300), nullable=True)
    project_ID = Column(INTEGER(6),info={'colanderalchemy': {'exclude': True}})
    experiment_description = Column(String(300))
    related_samples = Column(String(100), info={'colanderalchemy': {'description': 'Any related samples ID or these can be added'}})

    

    # enter this automatically base on user logged in
    #user_ID = Column(Integer, info={'colanderalchemy': {'exclude': True}})
  


#association tables not used
exp_has_publication = Table(
	'exp_has_publication', metadata,
	Column('publication_ID', ForeignKey('publication.publication_ID'), nullable=False, index=True),
    	Column('experiment_ID', ForeignKey('experiment.experiment_ID'), nullable=False, index=True)
)

project_has_experiment = Table(
    'project_has_experiment', metadata,
    Column('project_ID', ForeignKey('project.project_ID'), index=True),
    Column('experiment_ID', ForeignKey('experiment.experiment_ID'), primary_key=True)
)


class experimental_conditions(Base):
    __tablename__ = 'experimental_conditions'

    experimental_conditions_ID =Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    phase = Column(String(45), nullable=True)
    temperature = Column(Integer, default=0, nullable=True, info={'colanderalchemy': {'description': 'degrees centigrade'}})
    pressure = Column(Integer,default=0, nullable=True , info={'colanderalchemy': {'description': 'psi'}})
    experiment_ID = Column(INTEGER(4), info={'colanderalchemy': {'exclude': True}})


class data_aquisition(Base):
    __tablename__ = 'data_aquisition'

    data_aq_ID =Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    number_of_sample_scans = Column(INTEGER(11), nullable=True, default = 0)
    number_of_background_scans = Column(INTEGER(11), nullable=True, default = 0)
    scanner_velocity_KHz = Column(INTEGER(11), nullable=True, default = 0)
    resolution = Column(INTEGER(11), nullable=True, default = 0)
    start_frequency = Column(INTEGER(11), nullable=True, default = 0)
    end_frequency = Column(INTEGER(11), nullable=True, default = 0)
    optical_filter = Column(Enum('yes', 'no'), default='no')
    higher_range = Column('higher_range_(cm-1)', INTEGER(11), info={'colanderalchemy': {'description': 'cm^-1'}}, default = 0) 
    lower_range = Column('lower_range_(cm-1)', INTEGER(11), info={'colanderalchemy': {'description': 'cm^-1'}}, default = 0) 
    experiment_ID = Column(INTEGER(11),info={'colanderalchemy': {'exclude': True}})   
    
class spectrometer(Base):
    __tablename__ = 'spectrometer'

    spectrometer_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    instrument_manufacturer = Column(String(300))
    instrument_model = Column(String(300))
    light_source = Column(Enum('globar', 'laser', 'synchrotron', 'other',''), default = 'globar',nullable=True, info={'colanderalchemy': {'exclude': True}} )
    beamsplitter = Column(Enum('KBr', 'Mylar',''), default='KBr',nullable=True, info={'colanderalchemy': {'exclude': True}})
    detector__type = Column('detector_ type', Enum('DTGS', 'MCT Broad band', 'MCT narrow band', 'other',''), default='other', nullable=True, info={'colanderalchemy': {'exclude': True}})
    optics = Column(Enum('vacuum', 'purged', 'dry', 'atmospheric',''), default='dry',nullable=True, info={'colanderalchemy': {'exclude': True}})
    type_of_recording = Column(Enum('fourier transform', 'dispersive', 'tunable laser',''),  default = 'fourier transform',nullable=True, info={'colanderalchemy': {'exclude': True}})
    mode_of_recording = Column(Enum('transmission', 'ATR', 'transflectance', 'diffuse reflection',''), default='transmission',nullable=True, info={'colanderalchemy': {'exclude': True}})
    experiment_ID = Column(INTEGER(11), nullable=True , info={'colanderalchemy': {'exclude': True}})
   

class publication(Base):
    __tablename__ = 'publication'

    publication_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    experiment_ID = Column(INTEGER(11), nullable=True , info={'colanderalchemy': {'exclude': True}})
    publication_name = Column(String(1000))
    authors = Column('author', String(1000))
    link = Column(String(1000), info={'colanderalchemy': {'description': 'link to website'}})

    

class not_atr(Base):
    __tablename__ = 'not_atr'

    
    not_atr_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    sample_window_material = Column(Enum('CaF2', 'BaF2', 'ZnSe', 'ZnS', 'CdTe', 'KBr', 'KRS-5', 'other',''), default='CaF2',info={'colanderalchemy': {'exclude': True}})
    pathlength__if_known_ = Column('pathlength (if known)', INTEGER(11), info={'colanderalchemy': {'description': 'mm'}})
    multi_well_plate = Column('multi-well_plate', Enum('yes', 'no',''), default = 'no', info={'colanderalchemy': {'description': 'yes or no'}})
    product_code = Column( String(45),info={'colanderalchemy': {'description': 'If yes then what is the product code?'}})
    spectrometer_ID = Column(INTEGER(11),info={'colanderalchemy': {'exclude': True}})
                                                     
class atr(Base):
    __tablename__ = 'atr'

    atr_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    prism_size_mm = Column(INTEGER(11),nullable=True, default= 0 , info={'colanderalchemy': {'description': 'mm'}})
    number_of_reflections = Column(INTEGER(11),nullable=True, default = 0)
    prism_material = Column(Enum('Diamond', 'Ge', 'Si', 'KRS-5', 'ZnS', 'ZnSe', ''), default='Diamond', nullable=True, info={'colanderalchemy': {'exclude': True}})
    angle_of_incidence_degrees = Column(INTEGER(11),nullable=True, default = 0, info={'colanderalchemy': {'description': 'degrees'}})
    spectrometer_ID = Column(INTEGER(11),info={'colanderalchemy': {'exclude': True}})

class transflectance_diffuse(Base):
    __tablename__ = 'transf_diffuse'
    trans_diff_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    reflectance_device = Column(String(300), nullable=True)
    slide_material = Column(String(300),nullable=True)
    angle_of_incidence = Column(String(300),nullable=True,info={'colanderalchemy': {'description': 'In degrees'}})
    spectrometer_ID = Column(INTEGER(11),info={'colanderalchemy': {'exclude': True}})

#spectra


class spectra(Base):
    __tablename__ = 'spectra'

    spectra_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    format = Column(Enum('absorbance', 'transmittance', 'reflectance', 'log reflectance', 'kubelka munk', 'ATR spectrum', 'pas spectrum', ''), nullable=True, info={'colanderalchemy': {'exclude': True}})
    #add a spectra name column in future
    experiment_ID = Column(Integer,nullable=True)


class ft_processing(Base):
    __tablename__ = 'ft_processing'
    ft_processing_ID = Column(INTEGER(11), default = 0, primary_key=True, info={'colanderalchemy': {'exclude': True}})
    apodization__function = Column('apodization_ function', Enum('Blackman-Harris 3-Term','','Blackman-Harris 5-Term', 'Norton-Beer,weak', 'Norton-Beer,medium', 'Norton-Beer,strong', 'Boxcar', 'Triangular', 'Four point', 'other'))
    zero_filling_factor = Column(INTEGER(11), default = 0, info={'colanderalchemy': {'description': 'Si'}})
    non_linearity_correction = Column(Enum('yes', 'no',''),info={'colanderalchemy': {'description': 'yes or no'}})
    phase_correction_mode = Column(Enum('Mertz', 'Mertz signed', 'Power spectrum', 'Mertz no peak search', 'Mertz signed no peak search', 'Power spectrum no peak search',''))
    phase_resolution = Column(INTEGER(11) , default=0)
    experiment_ID = Column(ForeignKey('experiment.experiment_ID'))


class post_processing_and_deposited_spectra(Base):
    __tablename__ = 'post_processing_and_deposited_spectra'

    sample_power_spectrum = Column(String(45), info={'colanderalchemy': {'exclude':True}})
    background_power_spectrum = Column(String(45), info={'colanderalchemy': {'exclude':True}})
    initial_result_spectrum = Column(String(45), info={'colanderalchemy': {'exclude':True}})
    initial_result_spectrum_format = Column('initial result spectrum format', Enum('Blackman-Harris 3-Term','', 'Blackman-Harris 5-Term', 'Norton-Beer,weak', 'Norton-Beer,medium', 'Norton-Beer,strong', 'Boxcar', 'Triangular', 'Four point', 'other'), nullable=True)
    water_vapour = Column('water vapour', String(45))
    solvent = Column(String(45))
    solution_composition_item_1 = Column(String(45))
    solution_composition_item_2 = Column(String(45))
    other = Column(String(45))
    baseline_correction = Column(String(45))
    scaling = Column(String(45))
    second_derivative = Column('2nd_derivative', Enum('yes', 'no',''), default = 'no')
    method = Column(String(300))
    window_point_size_smoothing = Column('window_point_size/smoothing', String(45))
    final_published_spectrum = Column(String(45), info={'colanderalchemy': {'exclude':True}})
    final_published_spectrum_format = Column(Enum('absorbance', 'transmittance','', 'reflectance', 'log reflectance', 'Kubelka Munk', 'ATR spectrum', 'PAS spectrum'), default='absorbance')
    smoothing_method = Column(String(45))
    smoothing_parameters = Column(String(45))
    spectra_ID = Column(Integer, index=True, info={'colanderalchemy': {'exclude': True}})
    PPandD_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})




"""class FTIRModel(Base):
    This class is to create the main FTIRModel table with SQL alchemy 
    __tablename__ = 'FTIRModel'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    data = Column(Text, nullable=False)
    magic = Column(Text, nullable=False)
    
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_pages')"""

