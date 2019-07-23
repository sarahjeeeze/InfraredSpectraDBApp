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
from ..models import FTIRModel, Depositor, FourierTransformProcessing

import colander
import deform
import requests
from deform import Form

#imppot sqlalchemy 
from sqlalchemy import event
from sqlalchemy import *
from sqlalchemy.databases import mysql
from sqlalchemy.orm import relation, backref, synonym
from sqlalchemy.orm.exc import NoResultFound
from colanderalchemy import setup_schema
# MyModel is your SQLAlchemy model class
event.listen(FTIRModel, 'mapper_configured', setup_schema)
event.listen(Depositor, 'mapper_configured', setup_schema)

from deform.widget import Widget
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
        setup_schema(None, Depositor)
        schema = Depositor.__colanderalchemy__
        #schema2 = Depositor.__colanderalchemy__
        
        form = deform.Form(schema, buttons=('submit',))
        #form2 = deform.Form(schema2, buttons=('submit',))
        # We don't need to suppy all the values required by the schema
        # for an initial rpip endering, only the ones the app actually has
        # values for.  Notice below that we don't pass the ``name``
        # value specified by the ``Mapping`` schema.
      

        
        #return {'form':form}
        if request.POST:
            req = request.POST
            j = request._json_body__get        
                    
            print(json)
            #file = request.params['file']
            #file.write(file)    
            print(len(req))
            for i in req:
                    print(req[i])
                # i is the name of the dictionary pairs
                # r is the dictionary itself
            list = {}
            
            for item in req:
                    list[item] = req[item]
                    
            y = json.dumps(list)
            print(y)
            #name = request.params['name']
            #data = request.params['data']
            #magic = request.params['magic']# detect that the submit button was clicked
            controls = request.POST.items() # get the form controls
           # entereddetail = request.params
            #page = Depositor(y)
            request.dbsession.add(y)
            
        #session.commit()
            print(entereddetail)
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
            return{'form':form}

        
    # the form submission succeeded, we have the data
        
#code for uploading jcamp file

    
    


