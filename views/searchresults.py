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

from ..models import FTIRModel, User

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")


@view_config(route_name='results', renderer='../templates/results.jinja2')
def view_results(request):
    thisdict =	{
      "apple": "green",
      "banana": "yellow",
      "cherry": "red"
        }
    
    return (thisdict)
    
