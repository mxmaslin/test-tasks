from app import db


class DictMixin:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Crime(db.Model, DictMixin):
    __tablename__ = 'crime'

    id = db.Column(db.Integer, primary_key=True)
    crime_id = db.Column(db.Integer)
    crime_type = db.Column(db.String)
    report_date = db.Column(db.DateTime, index=True)
    offence_date = db.Column(db.DateTime)
    call_dt = db.Column(db.DateTime)
    disposition = db.Column(db.String)
    address = db.Column(db.String)

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))


class City(db.Model, DictMixin):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    crimes = db.relationship('Crime', backref='city')


class State(db.Model, DictMixin):
    __tablename__ = 'state'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    crimes = db.relationship('Crime', backref='state')


class Agency(db.Model, DictMixin):
    __tablename__ = 'agency'

    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer)
    address_type = db.Column(db.String)
    location = db.Column(db.String)

    crimes = db.relationship('Crime', backref='agency')
