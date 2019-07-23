"""

Project: FTIRDB
File: views/form.py

Version: v1.0
Date: 10.09.2018
Function: provides functions required for addAccount view

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

contains modules and function required to output a form based on the data in the
model using colander alchemy and deform.

creates a schema and then a form. 



============


"""
from pyramid.compat import escape
import re
from docutils.core import publish_parts
import json
import shutil

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.response import Response
from ..models import FTIRModel, User, atr, chemicals, data_aquisition, depositor, dried_film, experiment, experimental_conditions, fourier_transform_processing, gas, liquid, molecular_composition, molecule, not_atr, post_processing_and_deposited_spectra, project, protein, publication, sample, solid, spectra, spectrometer, state_of_sample

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
# MyModel is your SQLAlchemy model class
event.listen(FTIRModel, 'mapper_configured', setup_schema)
event.listen(atr, 'mapper_configured', setup_schema)
event.listen(state_of_sample, 'mapper_configured', setup_schema)

from deform.widget import Widget, FileUploadWidget
from deform.interfaces import FileUploadTempStore 
class Person(colander.MappingSchema):
        name = colander.SchemaNode(colander.String())
        age = colander.SchemaNode(colander.Integer(),
                              validator=colander.Range(0, 200))

class People(colander.SequenceSchema):
        person = Person()

class Schema(colander.MappingSchema):
        people = People()
schema = Schema()
myform = Form(schema,button=('submit',))
form = myform.render()

@view_config(route_name='jcampupload', renderer='../templates/jcampupload.jinja2')
def form(request):
        """amaaazing functoin that creates a schema using SQL alchemy model which then
        outputs data in to a rendered form
        input: specific model you want to create form from
        output: form including error catching

        see comments to understand how it works
        """
        #class Parent(schema):
            
        class All(colander.MappingSchema):
                setup_schema(None,atr)
                atrschema =atr.__colanderalchemy__
                setup_schema(None,chemicals)
                chemicalsschema =chemicals.__colanderalchemy__
                setup_schema(None,data_aquisition)
                data_aquisitionschema =data_aquisition.__colanderalchemy__
                setup_schema(None,depositor)
                depositorschema =depositor.__colanderalchemy__
                setup_schema(None,dried_film)
                dried_filmschema =dried_film.__colanderalchemy__
                setup_schema(None,experiment)
                experimentschema =experiment.__colanderalchemy__
                setup_schema(None,gas)
                gasschema =gas.__colanderalchemy__
                setup_schema(None,liquid)
                liquidschema =liquid.__colanderalchemy__
                setup_schema(None,molecular_composition)
                molecular_compositionschema =molecular_composition.__colanderalchemy__,
                setup_schema(None,molecule)
                moleculeschema =molecule.__colanderalchemy__
                setup_schema(None,not_atr)
                not_atrschema =not_atr.__colanderalchemy__
                setup_schema(None,project)
                projectschema =project.__colanderalchemy__
                setup_schema(None,protein)
                proteinschema =protein.__colanderalchemy__
                setup_schema(None,publication)
                publicationschema =publication.__colanderalchemy__
                setup_schema(None,sample)
                sampleschema =sample.__colanderalchemy__
                setup_schema(None,solid)
                solidschema =solid.__colanderalchemy__
                #setup_schema(None,spectrometer)
                #spectrometerschema =spectrometer.__colanderalchemy__,
                #setup_schema(None,state_of_sample)
                #state_of_sampleschema =state_of_sample.__colanderalchemy__
            
        form = All()
        form = deform.Form(form,buttons=('submit',))


        tmpstore = FileUploadTempStore()
        class Schema(colander.Schema):
            upload = colander.SchemaNode(
                deform.FileData(),
                widget=deform.widget.FileUploadWidget(tmpstore)
                )

        schema = Schema()
        #form = deform.Form(schema, buttons=('submit',))
        #del appstruct["xyz"]
        
        
        
        if 'submit' in request.POST:
           
            #name = request.params['name']
            #data = request.params['data']
            #magic = request.params['magic']# detect that the submit button was clicked
            controls = request.POST.items()
            pstruct = peppercorn.parse(controls)
            
            
            print(pstruct)
            count = 0
            end = len(pstruct) - 1
            new = {}
            for i in pstruct:
                count += 1 
                if count > 2 and count < end:
                    new[i] = pstruct[i]
            print(new)
            ok = ''
            count1 = 0
            #for key, value in new.items():
                    
            
            """prism_material = request.params['prism_material']
            angle_of_incidence_degrees = request.params['angle_of_incidence_degrees']
            number_of_reflections = request.params['number_of_reflections']
            prism_size_mm = request.params['prism_size_mm']
            spectrometer_ID = 6
            page = atr(spectrometer_ID=spectrometer_ID,prism_size_mm=prism_size_mm,number_of_reflections=number_of_reflections,
                       angle_of_incidence_degrees=angle_of_incidence_degrees,prism_material=prism_material)
            request.dbsession.add(page)"""
            
            # get the form controls

               #newfile = request.params['widget']
       
    
           
            
            #print(form)
            #with open(folder, 'w+') as f:
                #f.write(captured['uappload']['fp'].read())
            
            #page = FTIRModel(name=name,data=data,magic=magic)
            #request.dbsession.add(page)
            for i in controls:
                    print(i)
        #session.commit()
            
            #record = merge_session_with_post(record,request.POST.items())
            #page = Depositor(record)
            #request.dbsession.add(page)
            #print(controls)
            #page.creator = request.user
            #request.dbsession.add(page)
            obj = request.POST
            try:
                appstruct = form.validate(controls)
                one = form.schema.objectify(appstruct, obj)
                request.dbsession.add(one)
                request.dbsession.commit()
                print(one)
                next_url = request.route_url('view_page', pagename='name')
                return HTTPFound(location=next_url)# call validate
            except deform.ValidationFailure as e: # catch the exception
                return {'form':e.render()}
           
            
            
             # re-render the form with an exception
            
            
            #return{'form':appstruct}
        else:
            form = form.render()    
            
            return{'form':form}        
        
    # the form submission succeeded, we have the data
        
#code for uploading jcamp file

    
    


