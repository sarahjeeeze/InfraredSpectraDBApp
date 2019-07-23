"""

Project: FTIRDB
File: models/__init__.py

Version: v1.0
Date: 10.09.2018
Function: Initialise the data models

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description: This imports submodules which include broken down model files (eg. FTIRModel/users)
If a developer wants to add any models they must be imported here

It initialises an SQL alchemy database connection using the configuration settings located in
C:\ftirdb\development or C:\ftirdb\production depending on required enviroment.



============



"""

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .FTIRModel import FTIRModel, dried_film, atr, publication, not_atr, transflectance_diffuse, spectrometer, post_processing_and_deposited_spectra,data_aquisition, spectra, experimental_conditions, project_has_experiment, exp_has_publication, experiment, gas, molecule, protein, chemical, liquid, project, molecules_in_sample, sample, solid, state_of_sample
from .user import User

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.

    - When using scripts you should wrap the session in a manager yourself.
      For example::

          import transaction

          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)

    """
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('ftirdb.models')``.

    """
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    # use pyramid_retry to retry a request when transient exceptions occur
    config.include('pyramid_retry')

    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )
