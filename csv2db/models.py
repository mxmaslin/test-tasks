from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base 

from engine import engine

Base = declarative_base(bind=engine) 
metadata = Base.metadata  


class Crime(Base):
    __tablename__ = 'crime'

    id = Column(Integer, primary_key=True)
    crime_id = Column(Integer)
    crime_type = Column(String)
    report_date = Column(DateTime, index=True)
    offence_date = Column(DateTime)
    call_dt = Column(DateTime)
    disposition = Column(String)
    address = Column(String)

    city_id = Column(Integer, ForeignKey('city.id'))
    state_id = Column(Integer, ForeignKey('state.id'))
    agency_id = Column(Integer, ForeignKey('agency.id'))


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    crimes = relationship('Crime', backref='city')


class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    crimes = relationship('Crime', backref='state')


class Agency(Base):
    __tablename__ = 'agency'

    id = Column(Integer, primary_key=True)
    agency_id = Column(Integer)
    address_type = Column(String)
    location = Column(String)

    crimes = relationship('Crime', backref='agency')


metadata.drop_all()
metadata.create_all(engine)
