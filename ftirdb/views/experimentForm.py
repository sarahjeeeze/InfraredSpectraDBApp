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
import pathlib

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

from ..models import FTIRModel, dried_film, spectra, data_aquisition, post_processing_and_deposited_spectra, experimental_conditions, project_has_experiment, exp_has_publication, experiment, gas, molecule, protein, chemical, liquid, project, molecules_in_sample, sample, solid, state_of_sample


# regular expression used to find WikiWords



@view_config(route_name='experimentForm', renderer='../templates/experimentForm.jinja2')
def experimentForm(request):

   
    
    """ project form page """
    class All(colander.MappingSchema):
        setup_schema(None,experiment)
        experimentSchema=experiment.__colanderalchemy__
        setup_schema(None,experimental_conditions)
        conditionsSchema=experimental_conditions.__colanderalchemy__
        setup_schema(None,data_aquisition)
        data_aquisition_Schema=data_aquisition.__colanderalchemy__
        
    
    tables = All()
    form = deform.Form(tables,buttons=('submit',))
        
    if 'submit' in request.POST:
        #map columns
        controls = request.POST.items()

        controls = request.POST.items()     #call validate
        pstruct = peppercorn.parse(controls)
        print(pstruct)
        

        try:



                appstruct = form.validate(controls)
                experiment_description = request.params['experiment_description']
                exp = pstruct['experimentSchema'] # try to add to database
                print(exp)
                page = experiment(project_ID=0,**exp)
                request.dbsession.add(page)
                experiment_description= request.params['experiment_description']
                #retrieve last db entry for experiment ID 
                id = request.dbsession.query(experiment).order_by(experiment.experiment_ID.desc()).first()#link experiment column to related foreign keys
                #experiment_id = request.dbsession.query(experiment).filter_by(experiment_description=experiment_description).first()
                experiment_id = int(id.experiment_ID) 
                
                experimental_cond = pstruct['conditionsSchema']
                page = experimental_conditions(experiment_ID=experiment_id, **experimental_cond)
                request.dbsession.add(page)
                data_aq = pstruct['data_aquisition_Schema']
                page = data_aquisition(**data_aq, experiment_ID=experiment_id)
                request.dbsession.add(page)
                #experiment_id = request.dbsession.query(experiment).filter_by(experiment_description=experiment_description).first()
                
                next_url = request.route_url('experimentPage', experiment=experiment_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'experimentForm':e.render()}
           

        
    
    else:
        experimentForm = form.render()
        return{'experimentForm':experimentForm}

@view_config(route_name='experimentForm2', renderer='../templates/experimentForm2.jinja2')
def experimentForm2(request):

    
    
    """ project form page """
    class All(colander.MappingSchema):
        setup_schema(None,experiment)
        experimentSchema=experiment.__colanderalchemy__
        setup_schema(None,experimental_conditions)
        conditionsSchema=experimental_conditions.__colanderalchemy__
        setup_schema(None,data_aquisition)
        data_aquisition_Schema=data_aquisition.__colanderalchemy__
        
    
    tables = All()
    form = deform.Form(tables,buttons=('submit',))
        
    if 'submit' in request.POST:
        #map columns
        controls = request.POST.items()
        project_ID = request.matchdict['project_ID']
        controls = request.POST.items()     #call validate
        pstruct = peppercorn.parse(controls)
        print(pstruct)
        

        try:



                appstruct = form.validate(controls)
                experiment_description = request.params['experiment_description']
                exp = pstruct['experimentSchema'] # try to add to database
                print(exp)
                page = experiment(project_ID=project_ID,**exp)
                request.dbsession.add(page)
                experiment_description= request.params['experiment_description']
                #retrieve last db entry for experiment ID 
                id = request.dbsession.query(experiment).order_by(experiment.experiment_ID.desc()).first()#link experiment column to related foreign keys
                #experiment_id = request.dbsession.query(experiment).filter_by(experiment_description=experiment_description).first()
                experiment_id = int(id.experiment_ID) 
                
                experimental_cond = pstruct['conditionsSchema']
                page = experimental_conditions(experiment_ID=experiment_id, **experimental_cond)
                request.dbsession.add(page)
                data_aq = pstruct['data_aquisition_Schema']
                page = data_aquisition(**data_aq, experiment_ID=experiment_id)
                request.dbsession.add(page)
                #experiment_id = request.dbsession.query(experiment).filter_by(experiment_description=experiment_description).first()
                
                next_url = request.route_url('experimentPage', experiment=experiment_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'experimentForm':e.render()}
           

        
    
    else:
        experimentForm = form.render()
        return{'experimentForm':experimentForm}
    

    
    
@view_config(route_name='experimentPage', renderer='../templates/experimentPage.jinja2')

def experimentPage(request):

    """This page takes a project with project_ID in the URL and returns a page with a dictionary of
all the values, it also contains buttons for adding samples and experiments. When page is linked from here
the child/parent relationship is created"""

    


    search = request.matchdict['experiment']
    #search = request.params['body']
    searchdb = request.dbsession.query(experiment).filter_by(experiment_ID=search).all()
    dic = {}
    for u in searchdb:
            new = u.__dict__
            dic.update( new )
    search2 = request.dbsession.query(experimental_conditions).filter_by(experiment_ID=search).all()
    dic2 = {}
    for u in search2:
        new = u.__dict__
        dic2.update( new )
    search3 = request.dbsession.query(data_aquisition).filter_by(experiment_ID=search).all()
    dic3 = {}
    for u in search3:
        new = u.__dict__
        dic3.update( new )
    search4 = request.dbsession.query(spectra.spectra_ID).filter_by(experiment_ID=search).all()
    spec = {}
    #dic of related spectra
    for u in search4:
        num = u[0]
        search = request.dbsession.query(post_processing_and_deposited_spectra.final_published_spectrum).filter_by(spectra_ID=num).first()
        spec[(num)] = search[0]
    #dic of related spectra 'final published file name to download from experiment page'
    dic4 = {}
  
    print(spec)
    print('here')
    import random
    for k,v in spec.items():
        colory  = '#' + ("%06x" % random.randint(0, 0xFFFFFF))

        jcamp_dict =  JCAMP_reader(pathlib.PureWindowsPath('C:/ftirdb/ftirdb/data/infrared_spectra/' + spec[k]))
        print(k)
        plt.plot(jcamp_dict['x'], jcamp_dict['y'], label='filename', color=colory)
        plt.xlabel(jcamp_dict['xunits'])
        plt.ylabel(jcamp_dict['yunits'])
    plt.savefig(pathlib.PureWindowsPath('C:/ftirdb/ftirdb/static/experiment.png'))
     
                                                                                               
    
    if 'form.submitted' in request.params:       
        if request.params['form.submitted'] == 'Add spectrometer':
            #retrieve experiment ID and send to spectrometer page
            print(request)
            exp_ID = dic['experiment_ID']
            
            next_url = request.route_url('spectrometerForm', experiment_ID = exp_ID)
            return HTTPFound(location=next_url)
        else:
            next_url = request.route_url('spectraForm')
            return HTTPFound(location=next_url)
        #return HTTPFound(location=next_url)
        
    else:
        return {'experiment': dic,'spectra':spec,'conditions':dic2,'data_aquisition':dic3, 'dic4':dic4 }
    

            
