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

from ..models import FTIRModel, User, Spectra, Spectra_detail, Graph_experiment

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

@view_config(route_name='view_wiki')
def view_wiki(request):
    next_url = request.route_url('view_page', pagename='FrontPage')
    return HTTPFound(location=next_url)

@view_config(route_name='about', renderer='../templates/about.jinja2')
def view_about(request):
    return {}
#added function for searching db based on input parameters - returns list of relvant records
@view_config(route_name='searchdb', renderer='../templates/searchdb.jinja2')
def view_searchdb(request):
    
    if 'form.submitted' in request.params:
        search = request.params['body']
        print('ok')
        searchdb = request.dbsession.query(FTIRModel).filter(FTIRModel.name==search).all()
        count = 0

        dic = {}
        for item in searchdb:
            count += 1
            dic[item] = 'hello'

        dic = {str(k): v for k, v in dic.items()}
        return dic
        #need to work on getting it to return dictionary of all results
        #next_url = request.route_url('view_page', pagename=search)
        
        #return HTTPFound(location=next_url)
        
        #return dict(('<a href="%s">%s</a>' % (next_url, escape(search))))
    return {}   
    
        
        

@view_config(route_name='view_page', renderer='../templates/view.jinja2',
             permission='view')
def view_page(request):
    page = request.context.page

    def add_link(match):
        word = match.group(1)
        exists = request.dbsession.query(FTIRModel).filter_by(name=word).all()
        if exists:
            view_url = request.route_url('view_page', pagename=word)
            return '<a href="%s">%s</a>' % (view_url, escape(word))
        else:
            add_url = request.route_url('add_page', pagename=word)
            return '<a href="%s">%s</a>' % (add_url, escape(word))

    content = publish_parts(page.data, writer_name='html')['html_body']
    content = wikiwords.sub(add_link, content)
    edit_url = request.route_url('edit_page', pagename=page.name)
    return dict(page=page, content=content, edit_url=edit_url)

@view_config(route_name='edit_page', renderer='../templates/edit.jinja2',
             permission='edit')
def edit_page(request):
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

@view_config(route_name='add_page', renderer='../templates/edit.jinja2',
             permission='create')
def add_page(request):
    pagename = request.context.pagename
    if 'form.submitted' in request.params:
        body = request.params['body']
        body2 = request.params['body2']
        page = FTIRModel(name=pagename, data=body, magic=body2)
        page.creator = request.user
        request.dbsession.add(page)
        next_url = request.route_url('view_page', pagename=pagename)
        return HTTPFound(location=next_url)
    save_url = request.route_url('add_page', pagename=pagename)
    return dict(pagename=pagename, pagedata='', save_url=save_url)
