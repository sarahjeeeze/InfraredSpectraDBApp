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
#from ..models import PostProcessingAndDepositedSpectra

#jcampupload = PostProcessingAndDepositedSpectra

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
event.listen(jcampupload, 'mapper_configured', setup_schema)

import os
import uuid
import shutil


from deform.widget import Widget

"""@view_config(route_name='jcampupload', renderer='../templates/jcampupload.jinja2')

def add_portfolio_item(request):

    user = request.user
    # define store for uploaded files
    class Store(dict):
        def preview_url(self, name):
            return ""

    store = Store()
    # create a form schema
    class PortfolioSchema(colander.MappingSchema):
        description = colander.SchemaNode(colander.String(),
            #validator = length(max=300),
            widget = text_area,
            title = "Description, tell us a few short words desribing your picture")
        upload = colander.SchemaNode(
                deform.FileData(),
                widget=widget.FileUploadWidget(store))

    schema = PortfolioSchema()
    myform = Form(schema, buttons=('submit',), action=request.url)

    # if form has been submitted
    if 'submit' in request.POST:

        controls = request.POST.items()
        try:
            appstruct = myform.validate(controls)
        except ValidationFailure as e:
            return {'form':e.render(), 'values': False}
        # Data is valid as far as colander goes

        f = appstruct['upload']
        upload_filename = f['filename']
        extension = os.path.splitext(upload_filename)[1]
        image_file = f['fp']

        # Now we test for a valid image upload
        image_test = imghdr.what(image_file)
        if image_test == None:
            error_message = "I'm sorry, the image file seems to be invalid is invalid"
            return {'form':myform.render(), 'values': False, 'error_message':error_message,
            'user':user}


        # generate date and random timestamp
        pub_date = datetime.datetime.now()
        random_n = str(time.time())

        filename = random_n + '-' + user.user_name + extension
        upload_dir = tmp_dir
        output_file = open(os.path.join(upload_dir, filename), 'wb')

        image_file.seek(0)
        while 1:
            data = image_file.read(2<<16)
            if not data:
                break
            output_file.write(data)
        output_file.close()

        # we need to create a thumbnail for the users profile pic
        basewidth = 530
        max_height = 200
        # open the image we just saved
        root_location = open(os.path.join(upload_dir, filename), 'r')
        image = pilImage.open(root_location)
        if image.size[0] > basewidth:
            # if image width greater than 670px
            # we need to recduce its size
            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
            portfolio_pic = image.resize((basewidth,hsize), pilImage.ANTIALIAS)
        else:
            # else the image can stay the same size as it is
            # assign portfolio_pic var to the image
            portfolio_pic = image

        portfolio_pics_dir = os.path.join(upload_dir, 'work')

        quality_val = 90
        output_file = open(os.path.join(portfolio_pics_dir, filename), 'wb')
        portfolio_pic.save(output_file, quality=quality_val)

        profile_full_loc = portfolio_pics_dir + '/' + filename

        # S3 stuff
        new_key = user.user_name + '/portfolio_pics/' + filename
        key = bucket.new_key(new_key)
        key.set_contents_from_filename(profile_full_loc)
        key.set_acl('public-read')

        public_url = key.generate_url(0, query_auth=False, force_http=True)

        output_dir = os.path.join(upload_dir)
        output_file = output_dir + '/' + filename
        os.remove(output_file)
        os.remove(profile_full_loc)

        new_image = Image(s3_key=new_key, public_url=public_url,
         pub_date=pub_date, bucket=bucket_name, uid=user.id,
         description=appstruct['description'])
        DBSession.add(new_image)
        # add the new entry to the association table.
        user.portfolio.append(new_image)

        return HTTPFound(location = route_url('list_portfolio', request))

    return dict(user=user, form=myform.render())
def jcampupload(request):
        filename = request.POST['jdx'].filename

        input_file = request.POST['jdx'].file
        file_path = os.path.join('/tmp', '%s.jdx' % uuid.uuid4())
        temp_file_path = file_path + '~'

        input_file.seek(0)
        
        with open(temp_file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file, output_file)

    # Now that we know the file has been fully saved to disk move it into place.

        os.rename(temp_file_path, file_path)

        return Response('OK')"""
"""

class Schema(colander.Schema):
                
                upload = colander.SchemaNode(
                deform.FileData(),
                widget=deform.widget.FileUploadWidget(tmpstore)
                )
                
@view_config(route_name='jcampupload', renderer='../templates/jcampupload.jinja2')
def form(request):
        
        

        schema = Schema()
        jcampupload = deform.Form(schema, buttons=('submit',))
        return{'jcampupload':jcampupload }

""" """def form(request):
        amaaazing functoin that creates a schema using SQL alchemy model which then
        outputs data in to a rendered form
        input: specific model you want to create form from
        output: form including error catching

        see comments to understand how it works
       
        

        #return self.render_form(form, success=tmpstore.clear)
        setup_schema(None, jcampupload)
        schema = jcampupload.__colanderalchemy__
        
        form = deform.Form(schema, buttons=('submit',))
        
        
        if request.POST:
           
            #name = request.params['name']
            #data = request.params['data']
            #magic = request.params['magic']# detect that the submit button was clicked
            controls = request.POST.items() # get the form controls
            
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
                #return HTTPFound(location=next_url)# call validate
                return httpexceptions.HTTPFound(request.url)
            except deform.ValidationFailure as e: # catch the exception
                return {'form':e.render()}
           
            
            
             # re-render the form with an exception
            
            
            return{'form':appstruct}
        else:
            form = form.render()
      
            return{'form':form }
"""
        
    # the form submission succeeded, we have the data
        
#code for uploading jcamp file

    
    
"""

