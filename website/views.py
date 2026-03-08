from flask import Blueprint, render_template, request

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
    return render_template("add-appointment.html")

@views.route('/manage/add-appointment-purpose', methods=['GET', 'POST'])
def add_appointment_purpose():
    return render_template("add-appointment-purpose.html")

@views.route('/manage/add-location', methods=['GET', 'POST'])
def add_location():
    return render_template("add-location.html")

@views.route('/manage/add-provider', methods=['GET', 'POST'])
def add_provider():
    return render_template("add-provider.html")

@views.route('/view-appointments')
def view_appointments():
    return render_template("view-appointments.html")

@views.route('/view-providers')
def view_providers():
    return render_template("view-providers.html")