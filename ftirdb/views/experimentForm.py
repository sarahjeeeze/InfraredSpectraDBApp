"""

Project: FTIRDB
File: views/graph.py

Version: v1.0
Date: 10.09.2018
Function: Methods required for filling out experiment form and returning an experiment record

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

Outputs forms for front end and values to add to database, and error checking
Also contains views for outputting experiment records and all associated meta data as well as
hyperlinks to related projects


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

    """ Create the experiment form using colander alchemy and deform, use sql alchemy sessions to add the data to the database """
    #create schema for each table
    class All(colander.MappingSchema):
        setup_schema(None,experiment)
        experimentSchema=experiment.__colanderalchemy__
        setup_schema(None,experimental_conditions)
        conditionsSchema=experimental_conditions.__colanderalchemy__
        setup_schema(None,data_aquisition)
        data_aquisition_Schema=data_aquisition.__colanderalchemy__
        
    
    tables = All()
    #create the deform form
    form = deform.Form(tables,buttons=('submit',))
        
    if 'submit' in request.POST:

        controls = request.POST.items()
        #change structure from multidictionary to dictionary
        pstruct = peppercorn.parse(controls)
        print(pstruct)
        

        try:


                appstruct = form.validate(controls)#call validate
                experiment_description = request.params['experiment_description']
                exp = pstruct['experimentSchema']
                #use **kwargs to add all form fields to the database
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
                next_url = request.route_url('experimentPage', experiment=experiment_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'experimentForm':e.render()}
    
    else:
        experimentForm = form.render()
        #render the form as a dictionary
        return{'experimentForm':experimentForm}

@view_config(route_name='experimentForm2', renderer='../templates/experimentForm2.jinja2')
def experimentForm2(request):
    
    
    
    """ repeated from above but this time if experiment is added from the project page the project ID will be recorded """
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
        
        controls = request.POST.items()
        project_ID = request.matchdict['project_ID']#this is the only different field - get the related project ID
        controls = request.POST.items()     
        pstruct = peppercorn.parse(controls)
        

        try:

                appstruct = form.validate(controls)
                experiment_description = request.params['experiment_description']
                exp = pstruct['experimentSchema'] 
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

    """This page takes the experiment ID from the URL and returns a page with a dictionary of
all the values, it also contains buttons for adding samples and experiments."""


    search = request.matchdict['experiment']
    #Query database to retrieve all related information and output as dictionarys
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
	#plot all spectra related to the experiment on one graph	
        colory  = '#' + ("%06x" % random.randint(0, 0xFFFFFF))
        dic4[k] = colory
        jcamp_dict =  JCAMP_reader(os.path.join('ftirdb','data','infrared_spectra',  spec[k]))
        print(k)
        plt.plot(jcamp_dict['x'], jcamp_dict['y'], label='filename', color=colory)
        plt.xlabel(jcamp_dict['xunits'])
        plt.ylabel(jcamp_dict['yunits'])
    plt.savefig(os.path.join('ftirdb','static','experiment.png'))
    print(dic4)
                                                                                               
    
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
    

            
