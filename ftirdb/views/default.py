"""

Project: FTIRDB
File: views/default.py

Version: v1.0
Date: 10.09.2018
Function: contains a number of views which are accessed specified routes 

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:
============
views are ran when accessed by specified routes and the output is pushed to
a renderer.

This default files contains many functions that are called when certain pages
are accessed

May wish to split this in to more files to make it clearer which functions are
relating to what functions. 



"""
#import modules
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
from pyramid.compat import escape
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.response import Response
# import modules for creating forms
import colander
import deform
from deform import widget
#import models
from ..models import FTIRModel, User,  spectra, experiment, project, spectrometer, molecule, sample

@view_config(route_name='view_wiki')
def view_wiki(request):
    """function for viewing the front page of the databank
    may become redundant"""
    next_url = request.route_url('view_page', pagename='FrontPage')
    return HTTPFound(location=next_url)

@view_config(route_name='about', renderer='../templates/about.jinja2')
def view_about(request):
    """function for calling a basic page with an about page
    this about information can all be written in the jinja2 page as it is all static"""
    return {}
#added function for searching db based on input parameters - returns list of relvant records
@view_config(route_name='searchdb', renderer='../templates/searchdb.jinja2')
def view_searchdb(request):
    """function to search the database based on input parameters
    input: parameters to search on (currently just any word
    output: list of search results
    Jinja 2 will render these in to html"""
    
    if 'form.submitted' in request.params:
        #use a look up to find search term

        
        search = request.params['body']
        
        #need to work on getting it to return dictionary of all results
        next_url = request.route_url('results', results=search, table = request.params['table'])
        
        return HTTPFound(location=next_url)
        
        #return dict(('<a href="%s">%s</a>' % (next_url, escape(search))))
    
    return {}   
    


@view_config(route_name='view_page', renderer='../templates/view.jinja2',
             permission='view')
def view_page(request):
    """function to view a specific page once clicked on, retrieves data entry
    from database
    input: specific word/key
    output: all relevant data
    """
    page = request.context.page

    def add_link(match):
        word = match.group(1)
        exists = request.dbsession.query(project).filter_by(project_ID=word).all()
        if exists:
            view_url = request.route_url('view_page', pagename=word)
            return '<a href="%s">%s</a>' % (view_url, escape(word))
        else:
            add_url = request.route_url('add_page', pagename=word)
            return '<a href="%s">%s</a>' % (add_url, escape(word))

    content = publish_parts(page.data, writer_name='html')['html_body']
    #content = wikiwords.sub(add_link, content)
    edit_url = request.route_url('edit_page', pagename=page.name)
    return dict(page=page, content=content, edit_url=edit_url)

@view_config(route_name='edit_page', renderer='../templates/edit.jinja2',
             permission='edit')
def edit_page(request):
    """ function to allow you to edit a record
    input: fill in fields
    output: url with newly created or edited record
    """
    page = request.context.page
    if 'form.submitted' in request.params:
        page.data = request.params['body']
        page.magic = request.params['body2']
        next_url = request.route_url('view_page', pagename=page.name)
        return HTTPFound(location=next_url)
    return dict(
        pagename=page.name,
        pagedata=page.data,
        pagemagic=page.magic,
        save_url=request.route_url('edit_page', pagename=page.name),
        )

@view_config(route_name='add_page', renderer='../templates/addPage.jinja2')
def add_page(request):
    """function to add records to the database - also checks parameters within
    defined boundaries
    input: all relevant metadata fields including(name/body/body2/experiment
    output: new page with input data rendered or a error page
    """

    #pagename = request.context.pagename
    if 'form.submitted' in request.params:
        name = request.params['name']
        body = request.params['body']
        body2 = request.params['body2']
        
        experiment = request.params['experiment']
        if not experiment:
            return Response('{"error"}')
        page = FTIRModel(name=name, data=body, magic=body2)
        #page.creator = request.user
        request.dbsession.add(page)
        next_url = request.route_url('view_page', pagename=name)
        return HTTPFound(location=next_url)
    #save_url = request.route_url('add_page', pagename=pagename)
    #return dict(pagename=pagename, pagedata='', save_url=save_url)
    return {}
