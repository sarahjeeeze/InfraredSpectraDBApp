"""

Project: FTIRDB
File: models/user.py

Version: v1.0
Date: 10.09.2018
Function: Create the user table with SQL Alchemy model

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:
============
The file contains a function to create the user table model including functions
for ensuring the password is encrypted/hashed - using bcrypt


"""
#import necessary modules
import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    
)

from .meta import Base


class User(Base):
    """ The SQLAlchemy declarative model class for a User object. """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    role = Column(Text, nullable=False)
    institution = Column(String(45))
    country = Column(String(45))
    principle_investigator = Column(String(45))
    

    password_hash = Column(Text)

    def set_password(self, pw):
        """ Function to encrypt password when it is created using bcrypt """ 
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        """ Function to check password input is same as the encrypted one saved in the DB"""
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False
    

