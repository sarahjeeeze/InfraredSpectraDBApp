"""

Project: FTIRDB
File: views/addAccount.py

Version: v1.0
Date: 10.09.2018
Function: provides functions required for addAccount view

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

Contains functions required for adding a new account



============


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

from ..models import FTIRModel, User

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")


@view_config(route_name='add_account', renderer='../templates/addAccount.jinja2')
def view_results(request):
     """ function called when use wants to create a new account - takes input from a form
     Input: name, password, email address
     output: next url with new user account"""
     if 'form.submitted' in request.params:

        if not request.params['name']:
            raise ValueError("User must have an email")

        username = request.params['name']
        password = request.params['password']
        role = 'editor'
        example = User(name=username,role=role)
        example.set_password(password)
        email = request.params['email']
        request.dbsession.add(example)
    
        next_url = request.route_url('userArea', user=username)
        
        return HTTPFound(location=next_url)
     return {}



@view_config(route_name='userArea', renderer='../templates/userArea.jinja2')
def userArea(request):
    """ If user already exists or user account is creator - user is directed to
     user area - this function requests available information from the database"""
    user = request.context.page
    user = request.dbsession.query(User).filter_by(name=user.name).first()
    return{ "user" : user}
        
        
