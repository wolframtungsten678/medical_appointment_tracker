from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

from .models import User, Specialty
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/sign-in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')

        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        if user is None or not check_password_hash(user.password, password):
            flash("Invalid username or password.", "error")
        else:
            login_user(user)
            return redirect(url_for("views.index"))

    return render_template("sign_in.html")

@auth.route('/logout')
def logout():
    return "logout"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        confirmed_password = request.form.get('confirmed-password','')

        if not 4 <= len(username) <= 50:
            flash('Username must be between 4 and 50 characters', category='error')
        elif password != confirmed_password:
            flash('Passwords must match', category='error')
        elif len(password) < 9: 
            flash('Password must be at least 9 characters', category='error')
        else:
            user = User(
                username=username,
                password=generate_password_hash(password),
            )
            db.session.add(user)

            try:
                db.session.flush()

                initial_specialties = [
                    'Allergist',
                    'Audiology',
                    'Cardiology',
                    'Chiropractor',
                    'Dentist',
                    'Dermatology',
                    'ENT',
                    'Endocrinology',
                    'Gastroenterology',
                    'General Practitioner',
                    'Genetics',
                    'Gynecology',
                    'Hematology',
                    'Infectious Disease Specialist',
                    'Nephrology',
                    'Neurology',
                    'Neuropsychology',
                    'Occupational Therapy',
                    'Oncology',
                    'Ophthalmology',
                    'Optometry',
                    'Orthodontics',
                    'Orthopedics',
                    'Pain Management',
                    'Physical Therapy',
                    'Podiatry',
                    'Psychotherapy',
                    'Pulmonology',
                    'Rheumatology',
                    'Sleep Specialist',
                    'Urology',
                    'Vascular Surgeon'
                ]

                for specialty_name in initial_specialties:
                    db.session.add(
                        Specialty(
                            provider_specialty=specialty_name,
                            user_id=user.id,
                        )
                    )

                db.session.commit()

            except IntegrityError: 
                db.session.rollback()
                flash('Entered username is already taken.', category='error')
            else: 
                flash('Account created! Please sign in.', category='success')
                return redirect(url_for('auth.login'))

    return render_template("sign_up.html")