"""

Project: FTIRDB
File: views/graph.py

Version: v1.0
Date: 10.09.2018
Function: provides functions required for addAccount view

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

Contains functions required for viewing graphs based on jcamp files



============


"""
from pyramid.compat import escape
import re
from docutils.core import publish_parts
import matplotlib.pyplot as plt
from jcamp import JCAMP_reader, JCAMP_calc_xsec



import numpy as np

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.response import Response

from ..models import FTIRModel, User

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")


@view_config(route_name='graph', renderer='../templates/graph.jinja2')
def view_graph(request):
    """ function for viewing graph
    input: filename which can be retrieved from the DB
    output: rendered graph as png image.

    need to think how you can get radiobuttons to display overlays of graphs
    need to think about user seperate folders or how to save these files/store in db
    """
    
    filename = 'C:/ftirdb/ftirdb/data/infrared_spectra/ozone.jdx'
    jcamp_dict = JCAMP_reader(filename)
    print(jcamp_dict)
    #plt.plot(jcamp_dict['wavelengths'], jcamp_dict['xsec'])

    #plt.xlabel(jcamp_dict['xunits'])
    #plt.ylabel(jcamp_dict['yunits'])
    
    filename2 = 'C:/ftirdb/ftirdb/data/infrared_spectra/toluene.jdx'
    jcamp_dict2 = JCAMP_reader(filename2)
    print(jcamp_dict2)
    plt.figure(1)
    plt.plot(jcamp_dict2['x'], jcamp_dict2['y'], label = 'filename2', alpha=0.4, color='blue')
    plt.savefig('C:/ftirdb/ftirdb/static/fig.png', transparent=True)
    plt.figure(2)
    plt.plot(jcamp_dict2['x'], jcamp_dict2['y'], label = 'filename2', alpha=0.4, color='blue')
    plt.plot(jcamp_dict['x'], jcamp_dict['y'], label='filename', alpha = 0.7, color='red')
    #plt.savefig('C:/ftirdb/ftirdb/static/fig.png')
    #plt.plot(jcamp_dict2['x']-jcamp_dict['x'],jcamp_dict2['y']-jcamp_dict['y'], color = 'green')
    plt.savefig('C:/ftirdb/ftirdb/static/fig2.png', transparent=True)
    return{'graphname': 'ftirdb:static/fig.png', 'graphname2':'ftirdb:static/fig2.png' }
    

