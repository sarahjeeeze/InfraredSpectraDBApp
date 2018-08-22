from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    String,
)

from .meta import Base
from sqlalchemy.orm import relationship

class Spectra(Base):
    __tablename__ = 'Spectra'
    spectra_id = Column(Integer, primary_key=True)
    label = Column(String(32), nullable=False, unique=True)
    time = Column(Integer, nullable=False)


   


class Spectra_detail(Base):
    __tablename__ = 'Spectra_detail'
    spectra_id = Column(Integer, primary_key=True)
    index= Column(Integer, nullable=False, unique=True)
    value = Column(Integer, nullable=False)
    

 

class Graph_experiment(Base):
    __tablename__ = 'Graph_experiment'
    spectra_id = Column(Integer, primary_key = True)
    a = Column(Integer, nullable=False)
    b = Column(Integer, nullable=False)
    c = Column(Integer, nullable=False)
    d = Column(Integer, nullable=False)
