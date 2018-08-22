import os
import sys
import transaction

from pyramid.paster import bootstrap, setup_logging, get_appsettings
from sqlalchemy.exc import OperationalError
from pyramid.scripts.common import parse_vars
from .. import models
from ..models import FTIRModel, User, Spectra, Spectra_detail, Graph_experiment
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models.meta import Base

def setup_models(dbsession):
    model = models.FTIRModel.FTIRModel(name='one', value = 1)
    dbsession.add(model)
    
    


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)



def main(argv=sys.argv):
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
            creator=editor,
            data='This is the front page',
            magic='lala',
        )

        
        dbsession.add(model)
