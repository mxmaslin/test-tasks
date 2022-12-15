from datetime import datetime
from dataclasses import dataclass
from typing import List

from app import db


SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    return instance


class AsDictMixin:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@dataclass
class Crime(db.Model, AsDictMixin):
    __tablename__ = 'crime'

    id: int = db.Column(db.Integer, primary_key=True)
    crime_id: int = db.Column(db.Integer)
    crime_type: str = db.Column(db.String)
    report_date: datetime = db.Column(db.DateTime, index=True)
    offence_date: datetime = db.Column(db.DateTime)
    call_dt: datetime = db.Column(db.DateTime)
    disposition: str = db.Column(db.String)
    address: str = db.Column(db.String)

    city_id: int = db.Column(db.ForeignKey('city.id'))
    state_id: int = db.Column(db.ForeignKey('state.id'))
    agency_id: int = db.Column(db.ForeignKey('agency.id'))


@dataclass
class City(db.Model, AsDictMixin):
    __tablename__ = 'city'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String)
    crimes: List[Crime] = db.relationship(Crime, backref='city')


@dataclass
class State(db.Model, AsDictMixin):
    __tablename__ = 'state'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String)
    crimes: List[Crime] = db.relationship(Crime, backref='state')


@dataclass
class Agency(db.Model, AsDictMixin):
    __tablename__ = 'agency'

    id: int = db.Column(db.Integer, primary_key=True)
    agency_id: int = db.Column(db.Integer)
    address_type: str = db.Column(db.String)
    location: str = db.Column(db.String)
    crimes: List[Crime] = db.relationship(Crime, backref='agency')
