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

class FTIRModel(Base):
    __tablename__ = 'FTIRModel'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    data = Column(Text, nullable=False)
    magic = Column(Text, nullable=False)

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_pages')
