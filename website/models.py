from . import db
from flask_login import UserMixin

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
    appointment = db.relationship('Appointments')

class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(50))
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'))
    location = db.Column(db.String(100), db.ForeignKey('locations.id'))
    visit_purpose = db.Column(db.String(50), db.ForeignKey('visit_purpose.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_row_1 = db.Column(db.String(100))
    address_row_2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.Integer)
    travel_from_home = db.Column(db.Integer)
    travel_from_work = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appointments = db.relationship('Appointments')

class VisitPurpose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visit_purpose = db.Column(db.String(50))
    appointment_frequency = db.Column(db.String(50))
    scheduling_reminder = db.Column(db.Integer)
    scheduling_lead_time = db.Column(db.Integer)
    visit_duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appointments = db.relationship('Appointments')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    providers = db.relationship('Providers')
    appointments = db.relationship('Appointments')
    locations = db.relationship('Locations')
    visit_purpose = db.relationship('VisitPurpose')