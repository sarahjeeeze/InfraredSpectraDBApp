"""

Project: FTIRDB
File: routes.py

Version: v1.0
Date: 10.09.2018
Function: provide the web address route structures

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:
============
These routes are used to direct user to the correct views


"""
# import all required libraries
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    Allow,
    Everyone,
)

#******************************************

# import the models 
from .models import FTIRModel, dried_film, gas, publication, data_aquisition, experimental_conditions,spectrometer, project_has_experiment, exp_has_publication, experiment, liquid, project, molecules_in_sample, sample, solid, state_of_sample, molecule, chemical, protein
from .models.FTIRModel import spectra

def includeme(config):
    """Direct web address to correct page and python views """
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('view_wiki', '/')
    config.add_route('searchdb','/searchdb')
    #config.add_route('form','/form')
    config.add_route('projectform','/projectform')
    config.add_route('projectPage','/projectPage/{pagename}',factory=page_factory)
    config.add_route('sampleForm','/sampleForm')
    config.add_route('sampleForm2','/sampleForm2/{project_ID}')
    config.add_route('samplePage','/samplePage/{samplename}',factory=sample_page_factory)
    config.add_route('moleculeForm','/moleculeForm')
    config.add_route('moleculeForm2','/moleculeForm2/{sample_ID}')
    config.add_route('moleculePage','/moleculePage/{molecule_ID}')
    config.add_route('experimentForm','/experimentForm')
    config.add_route('spectrometerForm','/spectrometerForm/{experiment_ID}')
    config.add_route('spectrometerPage','/spectrometerPage/{spectrometer_ID}')
    config.add_route('experimentForm2','/experimentForm2/{project_ID}')
    config.add_route('experimentPage','/experimentPage/{experiment}')
    config.add_route('spectraForm','/spectraForm')
    config.add_route('spectraPage','/spectraPage/{spectra_ID}')
    
    config.add_route('results','/results/{results}/{table}')
    config.add_route('graph','/graph')
    config.add_route('about', '/about')
   # config.add_route('jcampupload', '/jcampupload')
    config.add_route('upload', '/upload')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('add_account','/add_account')
    config.add_route('add_page', '/add_page')
    config.add_route('userArea','/{user}/userArea', factory=user_factory)
    config.add_route('view_page', '/{pagename}', factory=page_factory)
    config.add_route('edit_page', '/{pagename}/edit_page',
                     factory=page_factory)

def new_page_factory(request):
    pagename = request.matchdict['pagename']
    if request.dbsession.query(FTIRModel).filter_by(name=pagename).count() > 0:
        next_url = request.route_url('edit_page', pagename=pagename)
        raise HTTPFound(location=next_url)
    return NewPage(pagename)

def user_factory(request):
    user = request.matchdict['user']
    page = request.dbsession.query(users).filter_by(name=user).first()
    if page is None:
        raise HTTPNotFound
    return PageResource(page)


class NewPage(object):
    def __init__(self, pagename):
        self.pagename = pagename

    def __acl__(self):
        return [
            (Allow, 'role:editor', 'create'),
            (Allow, 'role:basic', 'create'),
        ]

def page_factory(request):
    pagename = request.matchdict['pagename']
    page = request.dbsession.query(project).filter_by(project_ID=pagename).first()
    if page is None:
        raise HTTPNotFound
    return PageResource(page)


def sample_page_factory(request):
    pagename = request.matchdict['samplename']
    page = request.dbsession.query(sample).filter_by(sample_ID=pagename).first()
    if page is None:
        raise HTTPNotFound
    return PageResource(page)

def spectrometer_page_factory(request):
    pagename = request.matchdict['experiment_ID']
    page = request.dbsession.query(experiment).filter_by(experiment_ID=pagename).first()
    if page is None:
        raise HTTPNotFound
    return PageResource(page)

def molecule_page_factory(request):
    pagename = request.matchdict['molecule']
    page = request.dbsession.query(molecule).filter_by(molecule_ID=pagename).first()
    if page is None:
        raise HTTPNotFound
    return PageResource(page)



class PageResource(object):
    def __init__(self, page):
        self.page = page

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, Everyone, 'edit'),
            (Allow, Everyone, 'edit'),
        ]
