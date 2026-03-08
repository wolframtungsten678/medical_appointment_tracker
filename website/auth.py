from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    return render_template("sign_in.html")

@auth.route('/logout')
def logout():
    return "logout"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirmed-password')

        if len(username) < 4:
            flash('Username must be greater than 3 characters', category='error')
        elif password != confirmed_password:
            flash('Passwords must match', category='error')
        elif len(password) < 7: 
            flash('Password must be greater than 6 characters', category='error')
        else:
            flash('Account created!', category='success')

    return render_template("sign_up.html")