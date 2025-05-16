from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, current_app, jsonify
)
from .models import User
from . import db
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        try:
            # Get form data
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_pass = request.form.get('confirm_password')

            # Validation
            if not all([username, email, password, confirm_pass]):
                flash('All fields are required.', 'danger')
                return render_template('sign_up.html')

            # Check for existing username
            if User.query.filter_by(username=username).first():
                flash('Username already taken.', 'warning')
                return render_template('sign_up.html')

            # Check for existing email
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'warning')
                return render_template('sign_up.html')

            if len(password) < 8:
                flash('Password must be at least 8 characters long.', 'danger')
                return render_template('sign_up.html')

            if password != confirm_pass:
                flash('Passwords do not match.', 'danger')
                return render_template('sign_up.html')

            # Create new user
            new_user = User(
                username=username,
                email=email,
                profileImage=None
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            flash(f'Welcome, {username}! Your account has been created.', 'success')
            return redirect(url_for('views.profile'))

        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
            return render_template('sign_up.html')

    return render_template('sign_up.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)  # Always remember for better UX
            session.permanent = True  # Make session permanent
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('views.profile'))
            
        flash('Invalid email or password', 'danger')
        return render_template('login.html')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))





