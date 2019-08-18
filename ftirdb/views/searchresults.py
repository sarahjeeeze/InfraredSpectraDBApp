"""

Project: FTIRDB
File: routes.py

Version: v1.0
Date: 06.07.2019
Function: search results

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:
============

Search results with hyperlinks to records

"""
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
from sqlalchemy import or_
from ..models import FTIRModel, User, spectra, post_processing_and_deposited_spectra, protein, chemical, other, project, experiment, FTIRModel, spectra, experiment, project, spectrometer, molecule, sample

from sqlalchemy.types import String


@view_config(route_name='results', renderer='../templates/results.jinja2')
def view_results(request):
    #define look up tables
    tables = {
        "experiment": experiment,
        "project": project,
        "sample": sample,
        "molecule": molecule,
        "spectra": spectra,
        "spectrometer": spectrometer,
        "protein": protein,
        "chemical": chemical,
        "other": other
    }

    tables2 = {
        "experiment": experiment.experiment_ID,
        "project": project.project_ID,
        "sample": sample.sample_ID,
        "molecule": molecule.molecule_ID,
        "spectra": spectra.spectra_ID,
        "spectrometer": spectrometer.spectrometer_ID,
        "protein": protein.molecule_ID,
        "chemical": chemical.molecule_ID,
        "other": other.molecule_ID
    }

    search = request.matchdict['results']
    #table to be searched
    model = tables[request.matchdict['table']]
    model2 = tables2[request.matchdict['table']]

    print(model2)
    results = {}
    #could easily change this to like instead of ==
    #query the database using look up table values
    for col in model.__table__.columns:
        try:
            searchdb = request.dbsession.query(model2).filter(
                col == search).all()
            results[col.key] = searchdb

        except Exception as e:
            print(f"Unhandled error: {e}")
            continue

    dic3 = {}
    #create a dictionary with returned values with key as string 'output' and id value
    #and value as record id number to use in hyperlink

    for k, v in results.items():
        for i in v:
            dic3['output' + str(i[0])] = (i[0])

    ok = request.matchdict['table'] + 'Page'

    #return dictionary
    return {"dic": dic3, "table": ok}
