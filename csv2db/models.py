from datetime import datetime
from dataclasses import dataclass, field
from typing import List

from sqlalchemy.orm import registry, relationship

SQLALCHEMY_TRACK_MODIFICATIONS = False

from app import db

mapper_registry = registry()


class DictMixin:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@mapper_registry.mapped
@dataclass
class Crime(DictMixin):
    __tablename__ = 'crime'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(
        init=False, metadata={'sa': db.Column(db.Integer, primary_key=True)}
    )
    crime_id: int = field(metadata={'sa': db.Column(db.Integer)})
    crime_type: str = field(metadata={'sa': db.Column(db.String)})
    report_date: datetime = field(
        metadata={'sa': db.Column(db.DateTime, index=True)}
    )
    offence_date: datetime = field(metadata={'sa': db.Column(db.DateTime)})
    call_dt: datetime = field(metadata={'sa': db.Column(db.DateTime)})
    disposition: str = field(metadata={'sa': db.Column(db.String)})
    address: str = field(metadata={'sa': db.Column(db.String)})

    city_id: int = field(
        metadata={'sa': db.Column(db.ForeignKey('city.id'))}
    )
    state_id: int = field(
        metadata={'sa': db.Column(db.ForeignKey('state.id'))}
    )
    agency_id: int = field(
        metadata={'sa': db.Column(db.ForeignKey('agency.id'))}
    )


@mapper_registry.mapped
@dataclass
class City(DictMixin):
    __tablename__ = 'city'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(
        init=False, metadata={'sa': db.Column(db.Integer, primary_key=True)}
    )
    name: str = field(metadata={'sa': db.Column(db.String)})
    crimes: List[Crime] = field(
        default_factory=list,
        metadata={'sa': db.relationship(Crime, backref='city')}
    )


@mapper_registry.mapped
@dataclass
class State(DictMixin):
    __tablename__ = 'state'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(
        init=False, metadata={'sa': db.Column(db.Integer, primary_key=True)}
    )
    name: str = field(metadata={'sa': db.Column(db.String)})
    crimes: List[Crime] = field(
        default_factory=list,
        metadata={'sa': db.relationship(Crime, backref='state')}
    )


@mapper_registry.mapped
@dataclass
class Agency(DictMixin):
    __tablename__ = 'agency'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(
        init=False, metadata={'sa': db.Column(db.Integer, primary_key=True)}
    )
    agency_id: int = field(metadata={'sa': db.Column(db.Integer)})
    address_type: str = field(metadata={'sa': db.Column(db.String)})
    location: str = field(metadata={'sa': db.Column(db.String)})
    crimes: List[Crime] = field(
        default_factory=list,
        metadata={'sa': db.relationship(Crime, backref='agency')}
    )
