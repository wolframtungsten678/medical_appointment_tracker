from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .models import db, Providers, Locations, VisitPurpose, Appointments
from datetime import date, time, datetime
from sqlalchemy.orm import joinedload

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/manage')
def manage():
    return render_template("manage.html")

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

@views.route('/manage/add-appointment', methods=['GET', 'POST'])
def add_appointment():
    providers = db.session.execute(db.select(Providers).order_by(Providers.last_name)).scalars().all()
    purposes = db.session.execute(db.select(VisitPurpose).order_by(VisitPurpose.visit_purpose)).scalars().all()
    locations = db.session.execute(db.select(Locations).order_by(Locations.address_row_1)).scalars().all()

    if request.method == 'POST':
        appointment_date = date.fromisoformat(request.form['appointment-date'])
        appointment_time = time.fromisoformat(request.form['appointment-time'])
        appointment_datetime = datetime.combine(appointment_date, appointment_time)

        location_id = request.form.get('appointment-location', type=int)
        provider_id = request.form.get('provider-name', type=int)
        purpose_id = request.form.get('appointment-type', type=int)

        appointment = Appointments(
            appointment_datetime = appointment_datetime
        )

        if location_id is not None:
            selected_location = db.get_or_404(Locations, location_id)
            appointment.location=selected_location.id

        if provider_id is not None:
            selected_provider = db.get_or_404(Providers, provider_id)
            appointment.provider_id=selected_provider.id

        if purpose_id is not None:
            selected_purpose = db.get_or_404(VisitPurpose, purpose_id)
            appointment.visit_purpose=selected_purpose.id

        db.session.add(appointment)
        db.session.commit()

        return redirect('/success-add-appointment')

    return render_template("add-appointment.html", providers=providers, purposes=purposes, locations=locations)

@views.route('/manage/add-appointment-purpose', methods=['GET', 'POST'])
def add_appointment_purpose():
    purposes = db.session.execute(db.select(VisitPurpose).order_by(VisitPurpose.visit_purpose)).scalars().all()

    if request.method == 'POST':
        is_active = 'appt-reminder-needed' in request.form ##Converts checkbox to Boolean

        visit_purposes = VisitPurpose(
            visit_purpose = request.form['visit-purpose'],
            appointment_frequency = request.form['appointment-frequency'],
            scheduling_reminder = is_active,
            scheduling_lead_time = request.form['sched-lead-time'],
            visit_duration = request.form['visit-duration'],
        )

        db.session.add(visit_purposes)
        db.session.commit()

        return redirect('/success-appointment-purpose')

    return render_template("add-appointment-purpose.html", purposes=purposes)

@views.route('/manage/add-location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location = Locations(
            practice_name = request.form['practice-name'],
            address_row_1 = request.form['address-row-1'],
            address_row_2 = request.form['address-row-2'],
            city = request.form['city'],
            state = request.form['state'],
            zip_code = request.form['zip-code'],
            travel_from_home = request.form['travel-home'],
            travel_from_work = request.form['travel-work']
        ) 

        db.session.add(location) 
        db.session.commit()  

        return redirect('/success-location')

    return render_template("add-location.html")

@views.route('/manage/add-provider', methods=['GET', 'POST'])
def add_provider():
    dd_provider_locations = db.session.execute(db.select(Locations).order_by(Locations.address_row_1)).scalars().all()

    if request.method == 'POST':
        location_id = request.form.get('add-provider-location', type=str)
    
        provider = Providers(
            first_name = request.form['provider-first-name'],
            last_name = request.form['provider-last-name'],
            specialty_name = request.form['provider-specialty'],
            phone_number = request.form['provider-phone-number'],
            website = request.form['provider-website'],
            fax_number = request.form['provider-fax'],
            email = request.form['provider-email'],
            scheduling_type = request.form['scheduling-method']
        )

        if location_id is not None:
            selected_location = db.get_or_404(Locations, location_id)
            provider.locations.append(selected_location)

        db.session.add(provider)
        db.session.commit()

        return redirect('/success-provider')

    return render_template("add-provider.html", dd_provider_locations=dd_provider_locations)

@views.route('/manage/edit-appointment-purpose-select', methods=['GET', 'POST'])
def edit_appointment_purpose_select():
    appointment_purposes = db.session.execute(db.select(VisitPurpose).order_by(VisitPurpose.visit_purpose)).scalars().all()
    return render_template("edit-appointment-purpose-select.html", appointment_purposes=appointment_purposes)

@views.route('/manage/<int:purpose_id>')
def edit_appointment_purpose(purpose_id):
    purpose = db.first_or_404(db.select(VisitPurpose).where(VisitPurpose.id == purpose_id))
    return render_template("edit-appointment-purpose.html", purpose=purpose)

@views.route('/success-add-appointment')
def success_add_appointment():
    return render_template("success-add-appointment.html")

@views.route('/success-appointment-purpose')
def succcess_appt_purpose():
    return render_template("success-appointment-purpose.html")

@views.route('/success-provider')
def success_provider():
    return render_template("success-provider.html")

@views.route('/success-location')
def success_location():
    return render_template("success-location.html")

@views.route('/view-appointments')
def view_appointments():
    appointment_data = db.select(Appointments).options(
        joinedload(Appointments.provider),
        joinedload(Appointments.location_details),
        joinedload(Appointments.visit_purpose_details)
    ).order_by(Appointments.appointment_datetime)

    appointments = db.session.execute(appointment_data).unique().scalars().all()

    return render_template("view-appointments.html", appointments=appointments)

@views.route('/view-providers')
def view_providers():
    providers = db.session.execute(db.select(Providers).order_by(Providers.last_name)).scalars().all()

    return render_template("view-providers.html", providers=providers)