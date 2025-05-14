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

            session['user_id'] = new_user.id
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
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
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


@auth.route('/verify_password', methods=['POST'])
@login_required
def verify_password():
    if not current_user.is_authenticated:
        return jsonify({'valid': False, 'error': 'Not authenticated'}), 401
        
    data = request.get_json()
    current_password = data.get('current_password')
    
    if current_user.check_password(current_password):
        return jsonify({'valid': True})
    return jsonify({'valid': False})


@auth.route('/settings', methods=['POST'])
@login_required
def update_settings():
    if request.form.get('action') == 'update_password':
        current_password = request.form.get('current-password')
        new_password = request.form.get('new-password')
        confirm_password = request.form.get('confirm-password')

        # Input validation
        if not all([current_password, new_password, confirm_password]):
            return jsonify({
                'success': False,
                'error': 'All password fields are required'
            })

        if new_password != confirm_password:
            return jsonify({
                'success': False,
                'error': 'New passwords do not match'
            })

        # Verify current password
        if not current_user.check_password(current_password):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            })

        try:
            current_user.set_password(new_password)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Password updated successfully'
            })
        except Exception as e:
            db.session.rollback()
            print(f"Password update error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'An error occurred while updating password'
            })

    return jsonify({'success': False, 'error': 'Invalid action'})


