"""

Project: FTIRDB
File: scripts/initialize_db.py

Version: v1.0
Date: 10.09.2018
Function: running this programme creates the database 

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:
============
The database can not be created if it already exists.

If database already exists - it is necessary to delete existing DB and recreate
with new model. 


"""
#import relevant modules 

import os
import sys
import transaction

from pyramid.paster import bootstrap, setup_logging, get_appsettings
from sqlalchemy.exc import OperationalError
from pyramid.scripts.common import parse_vars

#import sql alchemy model

from .. import models
from ..models import FTIRModel, User, FTIRModel,spectra, data_aquisition,publication, experimental_conditions, project_has_experiment, exp_has_publication, experiment, molecule, protein, chemical,dried_film, gas, liquid, project, molecules_in_sample, sample, solid, state_of_sample
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models.meta import Base

def setup_models(dbsession):
    """ function to set up the main model """
    model = models.FTIRModel.FTIRModel(name='one', value = 1)
    dbsession.add(model)
    
    


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)



def main(argv=sys.argv):
    """ function to initiate transaction manager and enter initial data in to DB such
        as initial user """
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)
    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        editor = User(name='editor', role='editor')
        editor.set_password('editor')
        dbsession.add(editor)

        basic = User(name='basic', role='basic')
        basic.set_password('basic')
        dbsession.add(basic)

        spectra = Spectra(spectra_id=1, label='first_spectra', time = 25)
        dbsession.add(spectra)

        spectra_detail = Spectra_detail(spectra_id=1, index=1, value = 1)
        dbsession.add(spectra_detail)

        graph_experiment = Graph_experiment(spectra_id=12, a=1, b=2, c=3, d=4)
        dbsession.add(graph_experiment)
        
        model = FTIRModel(
            name='FrontPage',
            #creator=editor,
            data='This is the front page',
            magic='lala',
        )

        
        dbsession.add(model)
