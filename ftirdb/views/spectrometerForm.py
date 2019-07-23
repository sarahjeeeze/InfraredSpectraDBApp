"""

Project: FTIRDB
File: views/graph.py

Version: v1.0
Date: 10.09.2018
Function: provides functions required for addAccount view

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

Contains functions required for viewing graphs based on jcamp files



============


"""
from pyramid.compat import escape
import shutil

import re
from docutils.core import publish_parts
import matplotlib.pyplot as plt
from jcamp import JCAMP_reader, JCAMP_calc_xsec
import colander 
import deform
import peppercorn
import requests
from deform import Form, FileData
import os
#imppot sqlalchemy 
from sqlalchemy import event
from sqlalchemy import *
from sqlalchemy.databases import mysql
from sqlalchemy.orm import relation, backref, synonym
from sqlalchemy.orm.exc import NoResultFound
import colanderalchemy
from colanderalchemy import setup_schema


import numpy as np

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.response import Response
import deform
import colander
from deform.widget import Widget, FileUploadWidget
from deform.interfaces import FileUploadTempStore 
from ..models import FTIRModel, dried_film, atr, not_atr, transflectance_diffuse, spectrometer, data_aquisition,post_processing_and_deposited_spectra, experimental_conditions, spectra, project_has_experiment, exp_has_publication, experiment, gas, molecule, protein, chemical, liquid, project, molecules_in_sample, sample, solid, state_of_sample

# regular expression used to find WikiWords
light_source_choice = (('','- Select -'),('globar','globar'), ('laser','laser'), ('synchrotron','synchrotron'), ('other','other'),('',''))
beam_splitter_choice = (('','- Select -'),('KBr','KBr'),('Mylar', 'Mylar'),('other','other'),('',''))
detector_choice = (('','- Select -'),('DTGS','DTGS'), ('MCT Broad band', 'MCT Broad band'),('MCT narrow band','MCT narrow band'), ('other','other'),('',''))
optics_choice = (('','- Select -'),('vacuum','vacuum'),( 'purged','purged'),('dry','dry'), ('atmospheric','atmospheric'),('',''),('other','other'))
recording_choice = (('','- Select -'),('fourier transform','fourier transform'), ('dispersive','dispersive'), ('tunable laser','tunable laser'),('',''),('other','other'))
mode_choice = (('','- Select -'),('transmission','transmission'),( 'ATR','ATR'), ('transflectance', 'transflectance'), ('diffuse reflection','diffuse reflection'),('other','other'),('',''))
window_choice = (('','- Select -'), ('CaF2','CaF2'),( 'BaF2','BaF2'), ('ZnSe','ZnSe'),( 'ZnS','ZnS'),( 'CdTe','CdTe'), ('KBr','KBr'), ('KRS-5','KRS-5'),('other','other'),('',''))
prism_choice = (('','- Select -'),('Diamond','Diamond'),('Ge','Ge'), ('Si', 'Si'), ('KRS-5','KRS-5'),( 'ZnS','Zns'), ('ZnSe', 'ZnSe'),('',''),('other','other'))

@view_config(route_name='spectrometerForm', renderer='../templates/spectrometerForm.jinja2')
def spectrometerForm(request):
    
    """ project form page """
  
    tmpstore = FileUploadTempStore()
    exp = request.matchdict['experiment_ID']
    class Sample(colander.MappingSchema):
        setup_schema(None,spectrometer)
        spectrometerSchema =spectrometer.__colanderalchemy__
        light_source = colander.SchemaNode(
                colander.String(),
                default='',
                widget=deform.widget.SelectWidget(values=light_source_choice)
                  )
        beamsplitter = colander.SchemaNode(
                colander.String(),
                default='',
                widget=deform.widget.SelectWidget(values=beam_splitter_choice)
                  )
        detector = colander.SchemaNode(
                colander.String(),
                default='',
                widget=deform.widget.SelectWidget(values=detector_choice)
                  )
        optics = colander.SchemaNode(
                colander.String(),
                default='',
                widget=deform.widget.SelectWidget(values=optics_choice)
                  )
        type_of_recording = colander.SchemaNode(
                colander.String(),
                default='',
                widget=deform.widget.SelectWidget(values=recording_choice)
                  )
        mode_of_recording = colander.SchemaNode(
                colander.String(),
                default='',
                widget=deform.widget.SelectWidget(values=mode_choice)
                  )
        setup_schema(None,atr)
        atrSchema =atr.__colanderalchemy__
        prism = colander.SchemaNode(
                colander.String(),
                default='',
                widget=deform.widget.SelectWidget(values=prism_choice)
                  )
        setup_schema(None,not_atr)
        not_atrSchema =not_atr.__colanderalchemy__
        window = colander.SchemaNode(
                colander.String(),
                default='',
                widget=deform.widget.SelectWidget(values=window_choice)
                  )
        setup_schema(None,transflectance_diffuse)
        trans_diff_Schema =transflectance_diffuse.__colanderalchemy__
           
        
        
    form = Sample()

    form = deform.Form(form,buttons=('submit',))
    
     

        
    if 'submit' in request.POST:#
        controls = request.POST.items()

        try:
            #upload file functionality - sample_power_spectrum as initial example
                
                print(controls)
                appstruct = form.validate(controls)                
                pstruct = peppercorn.parse(controls)
                print(pstruct)
                
                optics = request.params['optics']
                beamsplitter = request.params['beamsplitter']
                type_of_recording = request.params['type_of_recording']
                mode_of_recording = request.params['mode_of_recording']
                detector = request.params['detector']
                light_source = request.params['light_source']
                prism = request.params['prism']
                window = request.params['window']
                                    
                
                #break through adding schema to db without having to manually enter each one
                """ok = pstruct['Spectrometerschema']     
                page = spectrometer(experiment_ID=exp,optics=optics,beamsplitter=beamsplitter,type_of_recording=type_of_recording,
                                    detector__type=detector,light_source=light_source,mode_of_recording=mode_of_recording,**ok)
                request.dbsession.add(page)
                
                
                #try the same for upload and file name to add to db
                pok = pstruct['atrSchema']
                page = atr(**pok,prism_material=prism)
                request.dbsession.add(page)

                naok = pstruct['not_atrSchema']
                page = not_atr(**naok,sample_window_material=window)
                request.dbsession.add(page)

                tran = pstruct['trans_diff_Schema']
                page = transflectance_diffuse(**tran)
                request.dbsession.add(page)
                appstruct = form.validate(controls) #call validate
                #need to fix this
                print(appstruct)
                
                experiment_id = request.dbsession.query(spectrometer).filter_by(optics=optics).first()
                spec_id = experiment_id.spectrometer_ID"""
                next_url = request.route_url('spectrometerPage', spectrometer_ID=1)
                return HTTPFound(location=next_url)
                
             
        except deform.ValidationFailure as e: # catch the exception
                return {'spectrometerForm':e.render()}
           

    else:
        
        spectrometerForm = form.render()
        return{'spectrometerForm':spectrometerForm}
    
        

@view_config(route_name='spectrometerPage', renderer='../templates/spectrometerPage.jinja2')

def spectrometerPage(request):

 """This page takes a project with project_ID in the URL and returns a page with a dictionary of
all the values, it also contains buttons for adding samples and experiments. When page is linked from here
the child/parent relationship is created"""



 if 'form.submitted' in request.params:
        
        if request.params['form.submitted'] == 'sample':
            #retrieve project ID and send to sample page
         return {'projectForm': 'sample'}
        else:
            return {'projectForm': 'experiment'}
            
        #next_url = request.route_url('projectPage', pagename=4)
        #return HTTPFound(location=next_url)
        
        
        
 else:
        search = request.matchdict['spectrometer_ID']
    #search = request.params['body']
        searchdb = request.dbsession.query(spectrometer).filter_by(spectrometer_ID=search).all()
        dic = {}
    #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            dic.update( new )
    
    #need to work on display of this 
        return {'spectrometerPage': dic }
    
    


