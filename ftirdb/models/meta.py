"""

Project: FTIRDB
File: models/meta.py

Version: v1.0
Date: 10.09.2018
Function: Initialise the data models

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:


Recommended naming convention used by Alembic, as various different database
providers will autogenerate vastly different names making migrations more
difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html



"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)
