"""

Project: FTIRDB
File: views/graph.py

Version: v1.0
Date: 10.09.2018
Function: provides functions required for sample form and sample record views

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

============


"""
#import functions
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

#import required modules
from ..models import sample, state_of_sample, molecules_in_sample, liquid, gas, solid, dried_film

# drop down choices
choices = (('', '- Select -'), ('gas', 'gas'), ('solid', 'solid'),
           ('liquid', 'liquid'), ('dried_film', 'dried_film'), ('', ''))


@view_config(route_name='sampleForm', renderer='../templates/sampleForm.jinja2')
def sampleForm(request):
    """ sample form view """

    #set up schema including the drop down

    class Sample(colander.MappingSchema):
        setup_schema(None, sample)
        sampleschema = sample.__colanderalchemy__

        setup_schema(None, molecules_in_sample)
        molecules_in_sample_schema = molecules_in_sample.__colanderalchemy__
        setup_schema(None, state_of_sample)
        state_of_sample_schema = state_of_sample.__colanderalchemy__
        state = colander.SchemaNode(
            colander.String(),
            default='',
            widget=deform.widget.SelectWidget(values=choices))

        setup_schema(None, liquid)
        liquidschema = liquid.__colanderalchemy__
        setup_schema(None, solid)
        solid_schema = solid.__colanderalchemy__
        setup_schema(None, gas)
        gas_schema = gas.__colanderalchemy__
        setup_schema(None, dried_film)
        dried_film_schema = dried_film.__colanderalchemy__

    form2 = Sample()
    #create form in deform
    form = deform.Form(form2, buttons=('submit',))

    #request project id related from address
    #project_id = request.matchdict['project_ID']

    if 'submit' in request.POST:

        #map columns
        controls = request.POST.items()
        pstruct = peppercorn.parse(controls)

        try:
            appstruct = form.validate(request.POST.items())  # call validate
            samples = pstruct['sampleschema']
            project_id = 1
            page = sample(project_ID=project_id, **samples)
            request.dbsession.add(page)

            sample_id = request.dbsession.query(sample).order_by(
                sample.sample_ID.desc()).first()
            sample_id = sample_id.sample_ID
            molecules = pstruct['molecules_in_sample_schema']
            page = molecules_in_sample(sample_ID=sample_id, **molecules)
            request.dbsession.add(page)
            state_sample = pstruct['state_of_sample_schema']
            state = request.params['state']
            page = state_of_sample(sample_ID=sample_id,
                                   state=state,
                                   **state_sample)
            request.dbsession.add(page)
            state_id = request.dbsession.query(state_of_sample).order_by(
                state_of_sample.state_of_sample_ID.desc()).first()
            state_id = (state_id.state_of_sample_ID)
            liq = pstruct['liquidschema']
            page = liquid(state_of_sample_ID=state_id, **liq)
            request.dbsession.add(page)
            gas2 = pstruct['gas_schema']
            page = gas(state_of_sample_ID=state_id, **gas2)
            request.dbsession.add(page)
            dried_film2 = pstruct['dried_film_schema']
            page = dried_film(state_of_sample_ID=state_id, **dried_film2)
            request.dbsession.add(page)
            solid2 = pstruct['solid_schema']
            page = solid(state_of_sample_ID=state_id, **solid2)
            request.dbsession.add(page)

            next_url = request.route_url('samplePage', samplename=sample_id)
            return HTTPFound(location=next_url)

        except deform.ValidationFailure as e:  # catch the exception
            return {'sampleForm': e.render()}

    else:

        sampleForm = form.render()
        return {'sampleForm': sampleForm}


@view_config(route_name='sampleForm2',
             renderer='../templates/sampleForm2.jinja2')
def sampleForm2(request):
    """ sample form for when sample is added from project page """

    #set up schema including the drop down

    class Sample(colander.MappingSchema):
        setup_schema(None, sample)
        sampleschema = sample.__colanderalchemy__

        setup_schema(None, molecules_in_sample)
        molecules_in_sample_schema = molecules_in_sample.__colanderalchemy__
        setup_schema(None, state_of_sample)
        state_of_sample_schema = state_of_sample.__colanderalchemy__
        state = colander.SchemaNode(
            colander.String(),
            default='',
            widget=deform.widget.SelectWidget(values=choices))

        setup_schema(None, liquid)
        liquidschema = liquid.__colanderalchemy__
        setup_schema(None, solid)
        solid_schema = solid.__colanderalchemy__
        setup_schema(None, gas)
        gas_schema = gas.__colanderalchemy__
        setup_schema(None, dried_film)
        dried_film_schema = dried_film.__colanderalchemy__

    form2 = Sample()
    #create form in deform
    form = deform.Form(form2, buttons=('submit',))

    #request project id related from address
    project_id = request.matchdict['project_ID']

    if 'submit' in request.POST:

        #map columns
        controls = request.POST.items()
        pstruct = peppercorn.parse(controls)

        try:
            appstruct = form.validate(request.POST.items())  # call validate
            samples = pstruct['sampleschema']
            page = sample(project_ID=project_id, **samples)
            request.dbsession.add(page)

            sample_id = request.dbsession.query(sample).order_by(
                sample.sample_ID.desc()).first()
            sample_id = sample_id.sample_ID
            molecules = pstruct['molecules_in_sample_schema']
            page = molecules_in_sample(sample_ID=sample_id, **molecules)
            request.dbsession.add(page)
            state_sample = pstruct['state_of_sample_schema']
            state = request.params['state']
            page = state_of_sample(sample_ID=sample_id,
                                   state=state,
                                   **state_sample)
            request.dbsession.add(page)
            state_id = request.dbsession.query(state_of_sample).order_by(
                state_of_sample.state_of_sample_ID.desc()).first()
            state_id = (state_id.state_of_sample_ID)
            liq = pstruct['liquidschema']
            page = liquid(state_of_sample_ID=state_id, **liq)
            request.dbsession.add(page)
            gas2 = pstruct['gas_schema']
            page = gas(state_of_sample_ID=state_id, **gas2)
            request.dbsession.add(page)
            dried_film2 = pstruct['dried_film_schema']
            page = dried_film(state_of_sample_ID=state_id, **dried_film2)
            request.dbsession.add(page)
            solid2 = pstruct['solid_schema']
            page = solid(state_of_sample_ID=state_id, **solid2)
            request.dbsession.add(page)

            next_url = request.route_url('samplePage', samplename=sample_id)
            return HTTPFound(location=next_url)

        except deform.ValidationFailure as e:  # catch the exception
            return {'sampleForm': e.render()}

    else:

        sampleForm = form.render()
        return {'sampleForm': sampleForm}


@view_config(route_name='samplePage', renderer='../templates/samplePage.jinja2')
def samplePage(request):
    """The view for all of the sample information associated with the sample ID - includes molecular composition,sample conditions,
    information on liquid,gas,solid or dried film """
    #form fields for adding a new molecule
    if 'submitted' in request.params:
        if request.params['submitted'] == 'Add molecule':
            search = request.matchdict['samplename']
            next_url = request.route_url('moleculeForm2', sample_ID=search)
            return HTTPFound(location=next_url)

        else:
            return {'projectForm': 'experiment'}

    else:
        search = request.matchdict['samplename']
        searchdb = request.dbsession.query(sample).filter_by(
            sample_ID=search).all()
        sampledic = {}
        #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            sampledic.update(new)
        searchdb = request.dbsession.query(state_of_sample).filter_by(
            sample_ID=search).all()
        searchdb2 = request.dbsession.query(state_of_sample).filter_by(
            sample_ID=search).first()

        stateofsampledic = {}
        for u in searchdb:
            new = u.__dict__
            stateofsampledic.update(new)

        state_ID = searchdb2.state_of_sample_ID
        searchdb = request.dbsession.query(
            liquid, gas, dried_film,
            solid).filter_by(state_of_sample_ID=state_ID).all()
        print(searchdb)
        print('here')
        statedic = {}

        for u in searchdb:
            for i in u:
                new = i.__dict__
                statedic.update(new)
        print(statedic)

        #need to work on display of this
        return {
            'samplePage': sampledic,
            'stateofsample': stateofsampledic,
            'statedic': statedic
        }
