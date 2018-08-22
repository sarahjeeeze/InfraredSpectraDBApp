from pyramid.compat import escape
import re
from docutils.core import publish_parts
import matplotlib.pyplot as plt
from jcamp import JCAMP_reader



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
    
    filename = 'C:/ftirdb/ftirdb/data/infrared_spectra/1-butene.jdx'
    jcamp_dict = JCAMP_reader(filename)
    plt.plot(jcamp_dict['x'], jcamp_dict['y'])
    plt.title(filename)
    plt.xlabel(jcamp_dict['xunits'])
    plt.ylabel(jcamp_dict['yunits'])
    plt.savefig('C:/ftirdb/ftirdb/static/fig.png')
    return{}
    

