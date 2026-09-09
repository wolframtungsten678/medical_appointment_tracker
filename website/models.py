from . import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, ForeignKey

provider_locations = db.Table(
    "provider_locations", 
    Column("Provider ID", Integer, ForeignKey('providers.id'), primary_key=True),
    Column("Location ID", Integer, ForeignKey('locations.id'), primary_key=True)
)

class Providers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    specialty_name = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    fax_number = db.Column(db.Integer)
    email = db.Column(db.String(50))
    website = db.Column(db.String(100))
    scheduling_type = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    locations = db.relationship('Locations', secondary=provider_locations, back_populates='providers')
    appointments = db.relationship('Appointments', foreign_keys='Appointments.provider_id', back_populates='provider')
    

class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_datetime = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(50))
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'))
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))
    visit_purpose = db.Column(db.Integer, db.ForeignKey('visit_purpose.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    provider = db.relationship('Providers', foreign_keys=provider_id, back_populates='appointments')
    location_details = db.relationship('Locations', foreign_keys=location, back_populates='appointments')
    visit_purpose_details = db.relationship('VisitPurpose', foreign_keys=visit_purpose, back_populates='appointments')

class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    practice_name = db.Column(db.String(100))
    address_row_1 = db.Column(db.String(100))
    address_row_2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    travel_from_home = db.Column(db.Integer)
    travel_from_work = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    appointments = db.relationship('Appointments', foreign_keys='Appointments.location', back_populates='location_details')
    providers = db.relationship('Providers', secondary=provider_locations, back_populates='locations')

class VisitPurpose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visit_purpose = db.Column(db.String(50))
    appointment_frequency = db.Column(db.String(50))
    scheduling_reminder = db.Column(db.Boolean)
    scheduling_lead_time = db.Column(db.Integer)
    visit_duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    appointments = db.relationship('Appointments', foreign_keys='Appointments.visit_purpose', back_populates='visit_purpose_details')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    providers = db.relationship('Providers', foreign_keys='Providers.user_id')
    appointments = db.relationship('Appointments', foreign_keys='Appointments.user_id')
    locations = db.relationship('Locations', foreign_keys='Locations.user_id')
    visit_purpose = db.relationship('VisitPurpose', foreign_keys='VisitPurpose.user_id')
