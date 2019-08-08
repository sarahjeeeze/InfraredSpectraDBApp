"""

Project: FTIRDB
File: views/graph.py

Version: v1.0
Date: 10.09.2018
Function: provides functions required the molecule form and to view molecule record

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

Contains functions required for viewing graphs based on jcamp files



============


"""
#import all modules required
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
import sqlalchemy
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

from ..models import sample, state_of_sample, molecules_in_sample, other, liquid, gas, solid, dried_film, molecule, protein, chemical




@view_config(route_name='moleculeForm', renderer='../templates/moleculeForm.jinja2')
def moleculeForm(request):
    
    """ The view for adding a molecule """

    #set up schema   
    class All(colander.MappingSchema):
        setup_schema(None,molecule)
        moleculeschema=molecule.__colanderalchemy__
        setup_schema(None,protein)
        proteinschema=protein.__colanderalchemy__
        setup_schema(None,chemical)
        chemschema=chemical.__colanderalchemy__
        setup_schema(None,other)
        otherschema=other.__colanderalchemy__
		
        
       
        
    form = All()
    #create form with deform
    form = deform.Form(form,buttons=('submit',))

    



    if 'submit' in request.POST:
              
        
  
        #map columns
        controls = request.POST.items()
        pstruct = peppercorn.parse(controls)
        
      
        try:

                appstruct = form.validate(request.POST.items()) #call validate
                #if accepted add items to database
                mole = pstruct['moleculeschema']
                moleculename = request.params['molecule_name']
                
                page = molecule(**mole)
                request.dbsession.add(page)
                molecule_id = request.dbsession.query(molecule).order_by(molecule.molecule_ID.desc()).first()
                molecule_id  = molecule_id.molecule_ID

                prot = pstruct['proteinschema']
                page = protein(**prot,molecule_ID=molecule_id)
                request.dbsession.add(page)
                
                print(molecule_id)
                chem = pstruct['chemschema']
                page = chemical(**chem,molecule_ID=molecule_id)
                request.dbsession.add(page)
                oth = pstruct['otherschema']
                page = other(**oth,molecule_ID=molecule_id)
                request.dbsession.add(page)
                
                next_url = request.route_url('moleculePage', molecule_ID=molecule_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'sampleForm':e.render()} #return error report
           

        
    
    else:
        
        sampleForm = form.render()
        return{'sampleForm':sampleForm}
@view_config(route_name='moleculeForm2', renderer='../templates/moleculeForm2.jinja2')
def moleForm(request):
    
    """ The view for adding a molecule in sequence with a sample"""
    #request sample_ID from the address
    sample_ID = request.matchdict['sample_ID']
    #create schema
    class All(colander.MappingSchema):
        setup_schema(None,molecule)
        moleculeschema=molecule.__colanderalchemy__
        setup_schema(None,protein)
        proteinschema=protein.__colanderalchemy__
        setup_schema(None,chemical)
        chemschema=chemical.__colanderalchemy__
        setup_schema(None,other)
        otherschema=other.__colanderalchemy__
        

        
        
    form = All()
    #create form with deform
    form = deform.Form(form,buttons=('submit',))

    



    if 'submit' in request.POST:
              
        
  
        #map columns
        controls = request.POST.items()
        pstruct = peppercorn.parse(controls)
        
        
        try:

                appstruct = form.validate(request.POST.items()) #call validate
                #if accepted add to the database
                mole = pstruct['moleculeschema']
                moleculename = request.params['molecule_name']
                
                page = molecule(**mole)
                request.dbsession.add(page)
                #find molecule id by sorting data in descending order and taking the first one
                molecule_id = request.dbsession.query(molecule).order_by(molecule.molecule_ID.desc()).first()
                molecule_id  = molecule_id.molecule_ID
                

                prot = pstruct['proteinschema']
                page = protein(**prot,molecule_ID=molecule_id)
                request.dbsession.add(page)
                
                print(molecule_id)
                chem = pstruct['chemschema']
                page = chemical(**chem,molecule_ID=molecule_id)
                request.dbsession.add(page)
                oth = pstruct['otherschema']
                page = other(**oth,molecule_ID=molecule_id)
                request.dbsession.add(page)
                
                next_url = request.route_url('moleculePage', molecule_ID=molecule_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'sampleForm':e.render()}
           

        
    
    else:
        
        sampleForm = form.render()
        return{'sampleForm':sampleForm}    
@view_config(route_name='moleculePage', renderer='../templates/moleculePage.jinja2')

def moleculePage(request):

    """This page takes returns all the data associated with a molecule record"""

    if 'form.submitted' in request.params:
        # if any buttonns added then actions can be specified here
        if 'form.submitted' == 'sample':
            
            return {'projectForm': 'sample'}
        else:
            return {'projectForm': 'experiment'}
            
   
        
    else:
        #query database for molecule ID in molecule
        # may want to use joins or additional querys to return additional info eg. related samples
        search = request.matchdict['molecule_ID']
        searchdb = request.dbsession.query(molecule).filter_by(molecule_ID=search).all()
        dic = {}
        for i in searchdb:
                new = i.__dict__
                dic.update( new )
        # search chemical, protein and other table for related details 
        searchprotein = request.dbsession.query(chemical,protein,other).filter_by(molecule_ID=search).all()
        moldic = {}
        for u in searchprotein:
            for i in u:
                new = i.__dict__
                moldic.update( new )
    
        return {'moleculePage': dic, 'moleculeInfo':moldic}
    
    
