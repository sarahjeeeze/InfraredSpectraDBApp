"""

Project: FTIRDB
File: views/auth.py

Version: v1.0
Date: 10.09.2018
Function: provides functions required for addAccount view

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

Contains functions required fo authorising a log in 



============


"""



from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import User


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    """ includes function for checking user name and encrypted password match
    input: name, password
    output: Url either for failed login or to user area 
    """
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('view_wiki')
    message = ''
    login = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = request.dbsession.query(User).filter_by(name=login).first()
        if user is not None and user.check_password(password):
            headers = remember(request, user.id)
            return HTTPFound(location=next_url, headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
        )

@view_config(route_name='logout')
    
def logout(request):
    """function called when user logs out
    input: reqeust to logout
    output: logged out screen or back to home page
    """
    headers = forget(request)
    next_url = request.route_url('view_wiki')
    return HTTPFound(location=next_url, headers=headers)

@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)
