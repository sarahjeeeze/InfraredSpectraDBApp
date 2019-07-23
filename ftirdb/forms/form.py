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
import requests
from deform import Form, FileData
import os
#imppot sqlalchemy 
from sqlalchemy import event
from sqlalchemy import *
from sqlalchemy.databases import mysql
from sqlalchemy.orm import relation, backref, synonym
from sqlalchemy.orm.exc import NoResultFound
from colanderalchemy import setup_schema
# MyModel is your SQLAlchemy model class
event.listen(FTIRModel, 'mapper_configured', setup_schema)
event.listen(atr, 'mapper_configured', setup_schema)

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

@view_config(route_name='form', renderer='../templates/form.jinja2')
def form(request):
        """amaaazing functoin that creates a schema using SQL alchemy model which then
        outputs data in to a rendered form
        input: specific model you want to create form from
        output: form including error catching

        see comments to understand how it works
        """
        setup_schema(None,atr)
        schema =atr.__colanderalchemy__
        atrschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,chemicals)
        schema =chemicals.__colanderalchemy__
        chemicalsschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,data_aquisition)
        schema =data_aquisition.__colanderalchemy__
        data_aquisitionschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,depositor)
        schema =depositor.__colanderalchemy__
        depositorschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,dried_film)
        schema =dried_film.__colanderalchemy__
        dried_filmschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,experiment)
        schema =experiment.__colanderalchemy__
        experimentschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,experimental_conditions)
        schema =experimental_conditions.__colanderalchemy__
        experimental_conditionsschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,fourier_transform_processing)
        schema =fourier_transform_processing.__colanderalchemy__
        fourier_transform_processingschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,gas)
        schema =gas.__colanderalchemy__
        gasschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,liquid)
        schema =liquid.__colanderalchemy__
        liquidschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,molecular_composition)
        schema =molecular_composition.__colanderalchemy__
        molecular_compositionschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,molecule)
        schema =molecule.__colanderalchemy__
        moleculeschema = deform.Form(schema, buttons=('submit',))
        
        setup_schema(None,not_atr)
        schema =not_atr.__colanderalchemy__
        not_atrschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,post_processing_and_deposited_spectra)
        schema =post_processing_and_deposited_spectra.__colanderalchemy__
        post_processing_and_deposited_spectraschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,project)
        schema =project.__colanderalchemy__
        projectschema = deform.Form(schema, buttons=('submit',))
      
        setup_schema(None,protein)
        schema =protein.__colanderalchemy__
        proteinschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,publication)
        schema =publication.__colanderalchemy__
        publicationschema = deform.Form(schema, buttons=('submit',))
        
        setup_schema(None,sample)
        schema =sample.__colanderalchemy__
        sampleschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,solid)
        schema =solid.__colanderalchemy__
        solidschema = deform.Form(schema, buttons=('submit',))
    
        setup_schema(None,spectrometer)
        schema =spectrometer.__colanderalchemy__
        spectrometerschema = deform.Form(schema, buttons=('submit',))
        setup_schema(None,state_of_sample)
        schema =state_of_sample.__colanderalchemy__
        state_of_sampleschema = deform.Form(schema, buttons=('submit',))

        tmpstore = FileUploadTempStore()
        class Schema(colander.Schema):
            upload = colander.SchemaNode(
                deform.FileData(),
                widget=deform.widget.FileUploadWidget(tmpstore)
                )

        schema = Schema()
        form = deform.Form(schema, buttons=('submit',))
        

        
        
        if request.POST:
           
            #name = request.params['name']
            #data = request.params['data']
            #magic = request.params['magic']# detect that the submit button was clicked
            controls = request.POST.items() # get the form controls

            #newfile = request.params['widget']
            thinking = request.POST
            print (thinking)
            folder = 'C:/ftirdb/ftirdb/views'
            if not os.path.exists(folder):
                    os.makedir(mypath)
                    print"Path is created"
            fname = folder + "/" + "test.txt"
            with open(fname,"w") as x:
                    x.write("thisis a boy")
            
            
            #print(form)
            #with open(folder, 'w+') as f:
                #f.write(captured['upload']['fp'].read())
            
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
            
            try:
                appstruct = form.validate(controls)
                
                next_url = request.route_url('view_page', pagename='name')
                return HTTPFound(location=next_url)# call validate
            except deform.ValidationFailure as e: # catch the exception
                return {'form':e.render()}
           
            
            
             # re-render the form with an exception
            
            
            return{'form':appstruct}
        else:
            form = form.render()    
            atrform=atrschema.render()
            chemicalsform=chemicalsschema.render()
            data_aquisitionform=data_aquisitionschema.render()
            depositorform=depositorschema.render()
            dried_filmform=dried_filmschema.render()
            experimentform=experimentschema.render()
            experimental_conditionsform=experimental_conditionsschema.render()
            fourier_transform_processingform=fourier_transform_processingschema.render()
            gasform=gasschema.render()
            liquidform=liquidschema.render()
            molecular_compositionform=molecular_compositionschema.render()
            moleculeform=moleculeschema.render()
            not_atrform=not_atrschema.render()
            post_processing_and_deposited_spectraform=post_processing_and_deposited_spectraschema.render()
            projectform=projectschema.render()
            proteinform=proteinschema.render()
            publicationform=publicationschema.render()
            sampleform=sampleschema.render()
            solidform=solidschema.render()
            spectrometerform=spectrometerschema.render()
            state_of_sampleform=state_of_sampleschema.render()
            return{'form':form,'liquidform': liquidform, 
                     'dried_filmform': dried_filmform,
                     'experimental_conditionsform': experimental_conditionsform, 'proteinform': proteinform, 'atrform': atrform,
                     'depositorform': depositorform, 'not_atrform': not_atrform, 'fourier_transform_processingform': fourier_transform_processingform,
                     'post_processing_and_deposited_spectraform': post_processing_and_deposited_spectraform, 'spectrometerform': spectrometerform,
                     'projectform': projectform, 'solidform': solidform, 'publicationform': publicationform, 'molecular_compositionform': molecular_compositionform,
                     'moleculeform': moleculeform, 'experimentform': experimentform, 'sampleform': sampleform, 
                     'gasform': gasform, 'state_of_sampleform': state_of_sampleform,
                     'data_aquisitionform': data_aquisitionform, 'chemicalsform': chemicalsform}


        
        
    # the form submission succeeded, we have the data
        
#code for uploading jcamp file

    
    


