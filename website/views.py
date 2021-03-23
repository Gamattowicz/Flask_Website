from flask import Blueprint, render_template, request, flash, jsonify, \
    redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is empty', category='error')
        else:
            new_note = Note(content=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Noted added!', category='success')
    return render_template('home.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Noted deleted!', category='success')
    return jsonify({})


@views.route('/user-list', methods=['GET', 'POST'])
@login_required
def user_list():
    return render_template('user_list.html', user=current_user,
                           users=User.query.all())


@views.route('/delete-user', methods=['POST'])
def delete_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User created successfully!', category='success')

    return jsonify({})


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        country = request.form.get('country')
        city = request.form.get('city')

        user = User.query.filter_by(email=current_user.email).first()
        if email == user.email:
            flash('Emails are the same!', category='error')
        elif len(email) < 5:
            flash('Email is too short! Must be greater than 4 characters.',
                  category='error')
        elif name == user.name:
            flash('Names are the same!', category='error')
        elif len(name) < 2:
            flash('Name is too short! Must be greater than 1 character.',
                  category='error')
        elif country == user.country:
            flash('Countries are the same!', category='error')
        elif len(country) < 2:
            flash('Country is not correct', category='error')
        elif city == user.city:
            flash('Cities are the same!', category='error')
        elif len(city) < 2:
            flash('City is not correct', category='error')
        else:
            user.email = email
            user.name = name
            user.country = country
            user.city = city
            db.session.commit()
            flash('Profile has been updated!', category='success')
            return redirect(url_for('views.home'))

    return render_template('profile.html', user=current_user,
                           email=current_user.email,
                           name=current_user.name,
                           country=current_user.country,
                           city=current_user.city)