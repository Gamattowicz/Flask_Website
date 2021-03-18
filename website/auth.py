from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint('auth', __name__)


@auth.route('/login', method=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        return redirect(url_for('home'))

    return render_template('login.html')


@auth.route('/logout', method=['POST', 'GET'])
def logout():
    return '<h1>Logout</h1>'


@auth.route('/sign-up', method=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(name) < 2:
            pass
        elif password1 != password2:
            pass
        elif password1 < 8:
            pass
        elif len(email) < 5:
            pass
        else:
            return redirect(url_for('home'))
    return render_template('sign_up.html')