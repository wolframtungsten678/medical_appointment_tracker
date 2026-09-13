from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from .models import db, Providers, Locations, VisitPurpose, Appointments, Specialty
from datetime import date, time, datetime
from sqlalchemy.orm import joinedload, Session

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def index():
    appointments = db.session.execute(db.select(Appointments).order_by(Appointments.appointment_datetime).filter_by(user_id=current_user.id)).scalars().all()
    today = datetime.today()

    return render_template("index.html", appointments=appointments, today=today)

@views.route('/about')
@login_required
def about():
    return render_template("about.html")

@views.route('/manage')
@login_required
def manage():
    return render_template("manage.html")

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

@views.route('/manage/add-appointment', methods=['GET', 'POST'])
@login_required
def add_appointment():
    providers = db.session.execute(db.select(Providers).order_by(Providers.last_name).filter_by(user_id=current_user.id)).scalars().all()
    purposes = db.session.execute(db.select(VisitPurpose).order_by(VisitPurpose.visit_purpose).filter_by(user_id=current_user.id)).scalars().all()
    locations = db.session.execute(db.select(Locations).order_by(Locations.address_row_1).filter_by(user_id=current_user.id)).scalars().all()

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

@views.route('/manage/edit-appointment-select')
@login_required
def edit_appointment_select():
    appointments = db.session.execute(db.select(Appointments).order_by(Appointments.appointment_datetime).filter_by(user_id=current_user.id)).scalars().all()

    return render_template("edit-appointment-select.html", appointments=appointments)

@views.route('/manage/appointments/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    appointment = db.first_or_404(db.select(Appointments).where(Appointments.id==appointment_id).filter_by(user_id=current_user.id))
    providers = db.session.execute(db.select(Providers).order_by(Providers.last_name).filter_by(user_id=current_user.id)).scalars().all()
    purposes = db.session.execute(db.select(VisitPurpose).order_by(VisitPurpose.visit_purpose).filter_by(user_id=current_user.id)).scalars().all()
    locations = db.session.execute(db.select(Locations).order_by(Locations.address_row_1).filter_by(user_id=current_user.id)).scalars().all()

    if request.method == 'POST':
        updated_appointment = db.session.get(Appointments, appointment_id)

        if updated_appointment is None: 
            return "Appointment not found.", 404

        updated_appointment_date = date.fromisoformat(request.form['appointment-date'])
        updated_appointment_time = time.fromisoformat(request.form['appointment-time'])
        updated_appointment_datetime = datetime.combine(updated_appointment_date, updated_appointment_time)
        updated_appointment.appointment_datetime = updated_appointment_datetime

        location_id = request.form.get('appointment-location', type=int)
        provider_id = request.form.get('provider-name', type=int)
        purpose_id = request.form.get('appointment-type', type=int)

        if location_id is not None:
            selected_location = db.get_or_404(Locations, location_id)
            updated_appointment.location=selected_location.id

        if provider_id is not None:
            selected_provider = db.get_or_404(Providers, provider_id)
            updated_appointment.provider_id=selected_provider.id

        if purpose_id is not None:
            selected_purpose = db.get_or_404(VisitPurpose, purpose_id)
            updated_appointment.visit_purpose=selected_purpose.id

        db.session.commit()

        return redirect('/success-edit-appointment')

    return render_template("edit-appointment.html", appointment=appointment, providers=providers, purposes=purposes, locations=locations)

@views.route('/manage/add-appointment-purpose', methods=['GET', 'POST'])
@login_required
def add_appointment_purpose():
    purposes = db.session.execute(db.select(VisitPurpose).order_by(VisitPurpose.visit_purpose).filter_by(user_id=current_user.id)).scalars().all()

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

@views.route('/manage/edit-location-select', methods=['GET', 'POST'])
@login_required
def edit_location_select():
    locations = db.session.execute(db.select(Locations).order_by(Locations.address_row_1).filter_by(user_id=current_user.id)).scalars().all()
    return render_template("edit-location-select.html", locations=locations)

@views.route('/manage/location/<int:location_id>', methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    location = db.first_or_404(db.select(Locations).where(Locations.id == location_id))
    if request.method == 'POST':
        updated_location = db.session.get(Locations, location_id)

        if updated_location is None: 
            return "Location not found.", 404

        updated_location.practice_name = request.form['practice-name']
        updated_location.address_row_1 = request.form['address-row-1']
        updated_location.address_row_2 = request.form['address-row-2']
        updated_location.city = request.form['city']
        updated_location.state = request.form['state']
        updated_location.zip_code = request.form['zip-code']
        updated_location.travel_from_home = request.form['travel-home']
        updated_location.travel_from_work = request.form['travel-work']

        db.session.commit()

        return redirect('/success-edit-location')

    return render_template("edit-location.html", location=location)

@views.route('/manage/add-location', methods=['GET', 'POST'])
@login_required
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

@views.route('/manage/edit-provider-select')
@login_required
def edit_provider_select():
    providers = db.session.execute(db.select(Providers).order_by(Providers.last_name).filter_by(user_id=current_user.id)).scalars().all()
    return render_template("edit-provider-select.html", providers=providers)

@views.route('/manage/providers/<int:provider_id>', methods=['GET','POST'])
@login_required
def edit_provider(provider_id):
    provider = db.first_or_404(db.select(Providers).where(Providers.id == provider_id))

    if request.method == 'POST':
        provider = db.session.get(Providers, provider_id)

        if provider is None: 
            return "Provider not found.", 404

        provider.first_name = request.form['provider-first-name']
        provider.last_name = request.form['provider-last-name']
        provider.specialty = request.form['provider-specialty']
        provider.phone_number = request.form['provider-phone-number']
        provider.website = request.form['provider-website']
        provider.fax_number = request.form['provider-fax']
        provider.email = request.form['provider-email']
        provider.scheduling_type = request.form['scheduling-method']

        db.session.commit()

        return redirect('/success-edit-provider')

    return render_template('edit-provider.html', provider=provider)


@views.route('/manage/add-provider', methods=['GET', 'POST'])
@login_required
def add_provider():
    dd_provider_locations = db.session.execute(db.select(Locations).order_by(Locations.address_row_1).filter_by(user_id=current_user.id)).scalars().all()
    specialties = db.session.execute(db.select(Specialty).order_by(Specialty.provider_specialty).filter_by(user_id=current_user.id)).scalars().all()    

    if request.method == 'POST':
        location_id = request.form.get('add-provider-location', type=str)
    
        provider = Providers(
            first_name = request.form['provider-first-name'],
            last_name = request.form['provider-last-name'],
            specialty = request.form['provider-specialty'],
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

    return render_template("add-provider.html", dd_provider_locations=dd_provider_locations, specialties=specialties)

@views.route('/manage/edit-appointment-purpose-select', methods=['GET', 'POST'])
@login_required
def edit_appointment_purpose_select():
    appointment_purposes = db.session.execute(db.select(VisitPurpose).order_by(VisitPurpose.visit_purpose).filter_by(user_id=current_user.id)).scalars().all()
    return render_template("edit-appointment-purpose-select.html", appointment_purposes=appointment_purposes)


@views.route('/manage/appointment-purpose/<int:purpose_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment_purpose(purpose_id):
    purpose = db.first_or_404(db.select(VisitPurpose).where(VisitPurpose.id == purpose_id))

    if request.method == 'POST':
        is_active = 'appt-reminder-needed' in request.form ##Converts checkbox to Boolean
        visit_purpose = db.session.get(VisitPurpose, purpose_id)

        if visit_purpose is None:
            return "Visit purpose not found.", 404

        visit_purpose.visit_purpose = request.form['visit-purpose']
        visit_purpose.appointment_frequency = request.form['appointment-frequency']
        visit_purpose.scheduling_reminder = is_active
        visit_purpose.scheduling_lead_time = request.form['sched-lead-time']
        visit_purpose.visit_duration = request.form['visit-duration']

        db.session.commit()

        return redirect('/success-edit-appointment-purpose')

    return render_template("edit-appointment-purpose.html", purpose=purpose)

@views.route('/success-add-appointment')
@login_required
def success_add_appointment():
    return render_template("success-add-appointment.html")

@views.route('/success-appointment-purpose')
@login_required
def success_appt_purpose():
    return render_template("success-appointment-purpose.html")

@views.route('/success-edit-appointment')
@login_required
def success_edit_appointment():
    return render_template("success-edit-appointment.html")

@views.route('/success-edit-appointment-purpose')
@login_required
def success_edit_appointment_purpose():
    return render_template("success-edit-appointment-purpose.html")

@views.route('/success-edit-location')
@login_required
def success_edit_location():
    return render_template("success-edit-location.html")

@views.route('/success-edit-provider')
@login_required
def success_edit_provider():
    return render_template("success-edit-provider.html")

@views.route('/success-provider')
@login_required
def success_provider():
    return render_template("success-provider.html")

@views.route('/success-location')
@login_required
def success_location():
    return render_template("success-location.html")

@views.route('/view-appointments')
@login_required
def view_appointments():
    appointment_data = db.select(Appointments).options(
        joinedload(Appointments.provider),
        joinedload(Appointments.location_details),
        joinedload(Appointments.visit_purpose_details)
    ).order_by(Appointments.appointment_datetime).filter_by(user_id=current_user.id)

    appointments = db.session.execute(appointment_data).unique().scalars().all()

    return render_template("view-appointments.html", appointments=appointments)

@views.route('/view-providers')
@login_required
def view_providers():
    providers = db.session.execute(db.select(Providers).order_by(Providers.last_name).filter_by(user_id=current_user.id)).scalars().all()

    return render_template("view-providers.html", providers=providers)