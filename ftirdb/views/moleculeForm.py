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
from deform import widget

from ..models import sample, state_of_sample, molecules_in_sample, liquid, gas, solid, dried_film, molecule, protein, chemical




@view_config(route_name='moleculeForm', renderer='../templates/moleculeForm.jinja2')
def moleForm(request):
    
    """ project form page """

   
    choices = ('1','2','3')    
    class All(colander.MappingSchema):
        setup_schema(None,molecule)
        moleculeschema=molecule.__colanderalchemy__
        
        setup_schema(None,protein)
        proteinschema=protein.__colanderalchemy__
        setup_schema(None,chemical)
        chemschema=chemical.__colanderalchemy__
        
        #protein = proteins(widget=deform.widget.SequenceWidget(orderable=True))

        
        
    form = All()
    print(form)
    #reqts = form['form1']['form'].get_widget_resources()
    form = deform.Form(form,buttons=('submit',))

    



    if 'submit' in request.POST:
              
        
  
        #map columns
        controls = request.POST.items()
        pstruct = peppercorn.parse(controls)
        
        #molecule
  
    
                 
                #format for db input - descriptive_name = request.params['descriptive_name']
        
      
        try:

                #appstruct = form.validate(controls) 

                mole = pstruct['moleculeschema']
                moleculename = request.params['molecule_name']
                
                page = molecule(**mole)
                request.dbsession.add(page)

                prot = pstruct['proteinschema']
                page = protein(**prot)
                request.dbsession.add(page)
                molecule_id = request.dbsession.query(molecule).order_by(molecule.molecule_ID.desc()).first()
                molecule_id  = molecule_id.molecule_ID
                print(molecule_id)
                chem = pstruct['chemschema']
                page = chemical(**chem)
                request.dbsession.add(page)
                
                next_url = request.route_url('moleculePage', molecule_ID=molecule_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'sampleForm':e.render()}
           

        
    
    else:
        
        sampleForm = form.render()
        return{'sampleForm':sampleForm}
@view_config(route_name='moleculeForm2', renderer='../templates/moleculeForm2.jinja2')
def moleForm(request):
    
    """ project form page """

    sample_ID = request.matchdict['sample_ID']
    choices = ('1','2','3')    
    class All(colander.MappingSchema):
        setup_schema(None,molecule)
        moleculeschema=molecule.__colanderalchemy__
        
        setup_schema(None,protein)
        proteinschema=protein.__colanderalchemy__
        setup_schema(None,chemical)
        chemschema=chemical.__colanderalchemy__
        
        #protein = proteins(widget=deform.widget.SequenceWidget(orderable=True))

        
        
    form = All()
    print(form)
    #reqts = form['form1']['form'].get_widget_resources()
    form = deform.Form(form,buttons=('submit',))

    



    if 'submit' in request.POST:
              
        
  
        #map columns
        controls = request.POST.items()
        pstruct = peppercorn.parse(controls)
        
        #molecule
  
    
                 
                #format for db input - descriptive_name = request.params['descriptive_name']
        
      
        try:

                #appstruct = form.validate(controls) 

                mole = pstruct['moleculeschema']
                moleculename = request.params['molecule_name']
                
                page = molecule(**mole)
                request.dbsession.add(page)

                prot = pstruct['proteinschema']
                page = protein(**prot)
                request.dbsession.add(page)
                molecule_id = request.dbsession.query(molecule).order_by(molecule.molecule_ID.desc()).first()
                molecule_id  = molecule_id.molecule_ID
                print(molecule_id)
                chem = pstruct['chemschema']
                page = chemical(**chem)
                request.dbsession.add(page)
                
                #fill out association table but only if form navigated from sample page
                
                next_url = request.route_url('moleculePage', molecule_ID=molecule_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'sampleForm':e.render()}
           

        
    
    else:
        
        sampleForm = form.render()
        return{'sampleForm':sampleForm}    
@view_config(route_name='moleculePage', renderer='../templates/moleculePage.jinja2')

def moleculePage(request):

    """This page takes a project with project_ID in the URL and returns a page with a dictionary of
all the values, it also contains buttons for adding samples and experiments. When page is linked from here
the child/parent relationship is created"""

    if 'form.submitted' in request.params:
        if 'form.submitted' == 'sample':
            
            return {'projectForm': 'sample'}
        else:
            return {'projectForm': 'experiment'}
            
        #next_url = request.route_url('projectPage', pagename=4)
        #return HTTPFound(location=next_url)
        
        
        
    else:
        print(request)
        search = request.matchdict['molecule_ID']
    #search = request.params['body']
        searchdb = request.dbsession.query(molecule).filter_by(molecule_ID=search).all()
        dic = {}
    #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            dic.update( new )
    
    #need to work on display of this 
        return {'moleculePage': dic}
    
    
