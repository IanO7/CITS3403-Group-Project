from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect(url_for('views.profile'))

    return render_template('sign_up.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        user     = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('views.profile'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
