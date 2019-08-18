"""

Project: FTIRDB
File: views/graph.py

Version: v1.0
Date: 10.09.2018
Function: provides functions required for inputting the spectra 

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

Contains functions required for viewing graphs based on jcamp files



============


"""
from pyramid.compat import escape
import shutil
from sqlalchemy import or_
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
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
from deform.widget import Widget, FileUploadWidget
from deform.interfaces import FileUploadTempStore
from ..models import FTIRModel, dried_film, data_aquisition, post_processing_and_deposited_spectra, experimental_conditions, spectra, project_has_experiment, exp_has_publication, experiment, gas, molecule, protein, chemical, liquid, project, molecules_in_sample, sample, solid, state_of_sample

#choices for drop downs
type_choices = (('sample power', 'sample power'), ('background power spectrum',
                                                   'background power spectrum'),
                ('initial result spectrum', 'initial result spectrum'), ('',
                                                                         ''))
format_choices = (('absorbance', 'absorbance'),
                  ('transmittance', 'transmittance'), ('reflectance',
                                                       'reflectance'),
                  ('log reflectance', 'log reflectance'), ('kubelka munk',
                                                           'kubelka munk'),
                  ('ATR spectrum', 'ATR spectrum'), ('pas spectrum',
                                                     'pas spectrum'), ('', ''))


@view_config(route_name='spectraForm',
             renderer='../templates/spectraForm.jinja2')
def spectraForm(request):
    """ view for adding all the spectra information """
    #create a temporary store for file uploads
    tmpstore = FileUploadTempStore()

    class Sample(colander.MappingSchema):
        setup_schema(None, spectra)
        spectraSchema = spectra.__colanderalchemy__
        format = colander.SchemaNode(
            colander.String(),
            default='',
            widget=deform.widget.SelectWidget(values=format_choices))
        sample_power_spectrum = colander.SchemaNode(
            deform.FileData(), widget=deform.widget.FileUploadWidget(tmpstore))
        background_power_spectrum = colander.SchemaNode(
            deform.FileData(), widget=deform.widget.FileUploadWidget(tmpstore))
        initial_result_spectrum = colander.SchemaNode(
            deform.FileData(), widget=deform.widget.FileUploadWidget(tmpstore))
        final_spectrum = colander.SchemaNode(
            deform.FileData(), widget=deform.widget.FileUploadWidget(tmpstore))
        setup_schema(None, post_processing_and_deposited_spectra)
        ppSchema = post_processing_and_deposited_spectra.__colanderalchemy__
        upload = colander.SchemaNode(
            deform.FileData(), widget=deform.widget.FileUploadWidget(tmpstore))

    form = Sample()

    form = deform.Form(form, buttons=('submit',))

    if 'submit' in request.POST:

        try:
            #appstruct = form.validate(request.POST.items()) #call validate
            #upload file functionality
            controls = request.POST.items()
            pstruct = peppercorn.parse(controls)
            # get filenames
            myfile = pstruct['sample_power_spectrum']['upload']
            background = pstruct['background_power_spectrum']['upload']
            init = pstruct['initial_result_spectrum']['upload']
            final = pstruct['final_spectrum']['upload']
            #using pure path as coding on windows and putting on to a linux server
            #specify where to store the files
            permanent_store = os.path.join('ftirdb', 'static', 'data')
            #open file and add file from temp store to permanent
            permanent_file = open(
                os.path.join(permanent_store, myfile.filename.lstrip(os.sep)),
                'wb')
            shutil.copyfileobj(myfile.file, permanent_file)
            myfile.file.close()
            #close file and repeat for each item
            permanent_file.close()
            #the same for back ground spectra
            permanent_file = open(
                os.path.join(permanent_store,
                             background.filename.lstrip(os.sep)), 'wb')
            shutil.copyfileobj(background.file, permanent_file)
            background.file.close()
            permanent_file.close()
            #the same for the initial spectra
            permanent_file = open(
                os.path.join(permanent_store, init.filename.lstrip(os.sep)),
                'wb')
            shutil.copyfileobj(init.file, permanent_file)
            init.file.close()
            permanent_file.close()
            #the same for final published spectra
            permanent_file = open(
                os.path.join(permanent_store, final.filename.lstrip(os.sep)),
                'wb')
            shutil.copyfileobj(final.file, permanent_file)
            final.file.close()
            permanent_file.close()
            print(myfile.filename)
            #break through adding schema to db without having to manually enter each one
            ok = pstruct['spectraSchema']
            # add other spectra details to the database
            format = request.params['format']
            page = spectra(**ok, format=format)
            request.dbsession.add(page)

            #add the filenames as strings to the database so they can be retreived
            pok = pstruct['ppSchema']
            sample_power_spectrum = myfile.filename
            background_power_spectrum = background.filename
            initial = init.filename
            final = final.filename
            searchdb = request.dbsession.query(spectra).order_by(
                spectra.spectra_ID.desc()).first()
            spectra_ID = searchdb.spectra_ID
            # add other spectra detail to the database
            page = post_processing_and_deposited_spectra(
                spectra_ID=spectra_ID,
                final_published_spectrum=final,
                sample_power_spectrum=sample_power_spectrum,
                background_power_spectrum=background_power_spectrum,
                initial_result_spectrum=initial,
                **pok)
            request.dbsession.add(page)

            next_url = request.route_url('spectraPage', spectra_ID=spectra_ID)
            return HTTPFound(location=next_url)

        except deform.ValidationFailure as e:  # catch the exception
            return {'spectraForm': e.render()}
    else:

        spectraForm = form.render()
        return {'spectraForm': spectraForm}


@view_config(route_name='spectraPage',
             renderer='../templates/spectraPage.jinja2')
def spectraPage(request):
    """This page returns all of the spectra related with a final published spectra and associated data, the spectra will be visible via radiobuttons"""

    if 'form.submitted' in request.params:
        #if any buttons added to page then the actions can be added here
        if request.params['form.submitted'] == 'sample':
            return {'projectForm': 'sample'}
        else:
            return {'projectForm': 'experiment'}

    else:
        # retreive spectra id from the address
        search = request.matchdict['spectra_ID']
        #query the database for the specra_ID's
        ppd = request.dbsession.query(post_processing_and_deposited_spectra
                                     ).filter_by(spectra_ID=search).all()

        depodic = {}
        for u in ppd:
            new = u.__dict__
            depodic.update(new)

        #plot each of the spectra on seperate figures using the dictionary values
        plt.figure(1)
        plt.tight_layout()
        # use os.join so it doesnt matter which OS you are using
        #plot the sample power spectrum
        filename = os.path.join('ftirdb', 'static', 'data',
                                depodic['sample_power_spectrum'])
        jcamp_dict = JCAMP_reader(filename)
        #use jcamp reader python lib to extract x and y values
        #set x axis to go in opposite direction
        plt.xlim(max(jcamp_dict['x']), min(jcamp_dict['x']))
        plt.plot(jcamp_dict['x'],
                 jcamp_dict['y'],
                 label='filename',
                 alpha=0.7,
                 color='blue')
        #plot the values

        plt.xlabel(jcamp_dict['xunits'])
        plt.ylabel(jcamp_dict['yunits'])
        plt.savefig(os.path.join('ftirdb', 'static', 'fig.png'),
                    bbox_inches="tight")

        plt.figure(2)
        #plot the background spectrum
        plt.tight_layout()
        filename2 = os.path.join('ftirdb', 'static', 'data', 'infrared_spectra',
                                 depodic['background_power_spectrum'])
        jcamp_dict2 = JCAMP_reader(filename2)

        plt.xlim(max(jcamp_dict2['x']), min(jcamp_dict2['x']))
        plt.plot(jcamp_dict2['x'],
                 jcamp_dict2['y'],
                 label='filename',
                 alpha=0.7,
                 color='green')
        plt.xlabel(jcamp_dict2['xunits'])
        plt.ylabel(jcamp_dict2['yunits'])

        plt.savefig(os.path.join('ftirdb', 'static', 'fig2.png'),
                    bbox_inches="tight")
        plt.figure(3)
        #plot the initial result spectrum
        plt.tight_layout()

        filename3 = os.path.join('ftirdb', 'static', 'data',
                                 depodic['initial_result_spectrum'])
        jcamp_dict3 = JCAMP_reader(filename3)
        plt.xlim(max(jcamp_dict3['x']), min(jcamp_dict3['x']))
        plt.plot(jcamp_dict3['x'],
                 jcamp_dict3['y'],
                 label='filename',
                 alpha=0.7,
                 color='red')
        plt.xlabel(jcamp_dict3['xunits'])
        plt.ylabel(jcamp_dict3['yunits'])
        plt.savefig(os.path.join('ftirdb', 'static', 'fig3.png'),
                    bbox_inches="tight")
        #plot the final published spectrum
        plt.figure(4)
        plt.tight_layout()

        filename4 = os.path.join('ftirdb', 'static', 'data',
                                 depodic['final_published_spectrum'])
        jcamp_dict4 = JCAMP_reader(filename4)
        plt.xlim(max(jcamp_dict4['x']), min(jcamp_dict4['x']))
        plt.plot(jcamp_dict3['x'],
                 jcamp_dict3['y'],
                 label='filename',
                 alpha=0.7,
                 color='magenta')
        plt.xlabel(jcamp_dict4['xunits'])
        plt.ylabel(jcamp_dict4['yunits'])
        plt.savefig(os.path.join('ftirdb', 'static', 'fig4.png'),
                    bbox_inches="tight")
        #file names ready to be downloaded
        jcampname1 = depodic['sample_power_spectrum']
        jcampname2 = depodic['background_power_spectrum']
        jcampname3 = depodic['initial_result_spectrum']
        jcampname4 = depodic['final_published_spectrum']

        return {
            'deop': depodic,
            'sample_power_spectrum': 'ftirdb:static/fig.png',
            'background_power_spectrum': 'ftirdb:static/fig2.png',
            'initial_result_spectrum': 'ftirdb:static/fig3.png',
            'filename': jcampname1,
            'filename2': jcampname2,
            'filename3': jcampname3,
            'filename4': jcampname4
        }
