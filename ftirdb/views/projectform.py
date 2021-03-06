"""

Project: FTIRDB
File: views/projectForm.py

Version: v1.0
Date: 10.08.2019
Function: provides functions required for adding and viewing a project

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

============


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
import numpy
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
import pathlib
from pathlib import Path

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

from ..models import project, experiment, spectrometer, post_processing_and_deposited_spectra, spectra, sample, publication


#view for the project form
@view_config(route_name='projectform',
             renderer='../templates/projectform.jinja2')
def projectform(request):
    """ project form page """

    #create the schema using colander alchemy
    class All(colander.MappingSchema):
        setup_schema(None, project)
        projectSchema = project.__colanderalchemy__
        setup_schema(None, publication)
        publicationSchema = publication.__colanderalchemy__

    # create the form using deform
    form = deform.Form(All(), buttons=('submit',))

    if 'submit' in request.POST:

        #retreive results and deserialize using peppercorn
        controls = request.POST.items()
        print(controls)
        pstruct = peppercorn.parse(controls)
        print(controls)

        try:
            # call validate on request.POST.items() 
            appstruct = form.validate(request.POST.items())

            #if no exceptions then add data to databank - pstruct must come after validation for error form to render
            #example of retrieving the form paramater 1 by 1 which may be useful if you want to manipulate the data before entering to the databank
            descriptive_name = request.params['descriptive_name']
            related_experiments_ID = request.params['related_experiments_ID']
            items = pstruct['publicationSchema']

            page = project(descriptive_name=descriptive_name,
                           related_experiments_ID=related_experiments_ID)

            request.dbsession.add(page)

            project_id = request.dbsession.query(project).order_by(
                project.project_ID.desc()).first()
            project_id = project_id.project_ID
            #example of adding data using **kwargs - the most efficient way
            page = publication(experiment_ID=project_id, **items)
            request.dbsession.add(page)
            #return project page
            next_url = request.route_url('projectPage', pagename=project_id)
            return HTTPFound(location=next_url)

        except deform.ValidationFailure as e:  # catch the exception
            return {'projectForm': e.render()}

    else:
        #render the form
        projectForm = form.render()
        return {'projectForm': projectForm}


@view_config(route_name='projectPage',
             renderer='../templates/projectPage.jinja2')
def projectPage(request):
    """This page takes a project with project_ID in the URL and returns a page with a dictionary of
all the values for the project, associated experiments and publication data, it also contains buttons for adding samples and experiments."""

    if 'submitted' in request.params:

        if request.params['submitted'] == 'Add sample':
            #button to add a new sample, also sending the project id to link the records
            search = request.matchdict['pagename']
            next_url = request.route_url('sampleForm2', project_ID=search)
            return HTTPFound(location=next_url)

        else:
            #saame as above but for experiment
            search = request.matchdict['pagename']
            next_url = request.route_url('experimentForm2', project_ID=search)
            return HTTPFound(location=next_url)

    else:
        search = request.matchdict['pagename']
        #return project info related to ID in url by querrying the databank

        searchdb = request.dbsession.query(project).filter_by(
            project_ID=search).all()
        projectdic = {}
        for u in searchdb:
            new = u.__dict__
            projectdic.update(new)
        #return experiment ID's 
        searchexp = request.dbsession.query(experiment).filter_by(
            project_ID=search).all()

        expdic = {}
        #return related experiments as a dictionary
        for u in searchexp:
            new = u.__dict__
            expdic.update(new)

    #return samples related to project ID in a dictionary

        samples = {}

        search2 = request.dbsession.query(
            sample.sample_ID).filter_by(project_ID=search).all()
    #turn list of objects in to a dictionary

        for u in search2:
            searchexp3 = request.dbsession.query(
                sample.descriptive_name).filter_by(sample_ID=u[0]).first()
            num = u[0]
            samples[searchexp3[0]] = num

    #return experiment IDs related to project ID, use try and except in case no results are returned
        exp_ID = request.dbsession.query(
            experiment.experiment_ID).filter_by(project_ID=search).first()

        try:
            searchexp2 = request.dbsession.query(
                experiment.experiment_ID).filter_by(project_ID=search).all()
            exp_ID = exp_ID[0]
        except:
            exp_ID = 0

        exper_IDs = {}
    #turn list of experiment_ID as object into a dictionary of experiment ID's

        for u in searchexp2:
            searchexp3 = request.dbsession.query(
                experiment.name).filter_by(experiment_ID=u[0]).first()
            num = u[0]
            exper_IDs[searchexp3[0]] = num

    #return spectra associated
        spectradic = {}
        search = request.dbsession.query(spectra).filter_by(
            experiment_ID=exp_ID).all()
        for u in search:
            new = u.__dict__
            spectradic.update(new)

        try:
            also = request.dbsession.query(
                spectra.spectra_ID).filter_by(experiment_ID=exp_ID).first()
            ppd_ID = also[0]

        except:
            ppd_ID = 0
        #retreive related spectra
        search2 = request.dbsession.query(post_processing_and_deposited_spectra
                                         ).filter_by(spectra_ID=ppd_ID).all()
        depodic = {}
        for u in search2:
            new = u.__dict__
            depodic.update(new)

    

        #retrieve publication information

        publicationdic = {}
        search = request.matchdict['pagename']
       
        search = request.dbsession.query(publication).filter_by(
            experiment_ID=search).all()
        for u in search:
            new = u.__dict__
            publicationdic.update(new)
        #return dictinarys to template
        return {
            'dic': projectdic,
            'expdic': expdic,
            'exper': exper_IDs,
            'samples': samples,
            'publication': publicationdic
        }
