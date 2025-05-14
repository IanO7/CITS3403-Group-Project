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


@auth.route('/verify_password', methods=['POST'])
@login_required
def verify_password():
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({
            'valid': False,
            'error': 'Authentication required'
        }), 401

    try:
        # Get JSON data with explicit content type check
        if not request.is_json:
            return jsonify({
                'valid': False,
                'error': 'Content-Type must be application/json'
            }), 400

        data = request.get_json()
        current_password = data.get('current_password')
        
        if not current_password:
            return jsonify({
                'valid': False,
                'error': 'Password is required'
            }), 400
        
        # Verify password
        is_valid = current_user.check_password(current_password)
        print(f"Debug - Password verification for {current_user.username}: {'success' if is_valid else 'failed'}")
        
        return jsonify({
            'valid': is_valid,
            'message': 'Password verified' if is_valid else 'Invalid password'
        }), 200 if is_valid else 400
    
    except Exception as e:
        print(f"Password verification error: {str(e)}")
        return jsonify({
            'valid': False,
            'error': 'Server error during verification'
        }), 500


@auth.route('/settings', methods=['POST'])
@login_required
def update_settings():
    if request.form.get('action') == 'update_password':
        try:
            current_password = request.form.get('current-password')
            new_password = request.form.get('new-password')

            print("DEBUG: current_password from form:", current_password)
            print("DEBUG: new_password from form:", new_password)
            print("DEBUG: All form keys:", list(request.form.keys()))

            print(f"Debug - Updating password for user: {current_user.username}")
            print(f"Debug - Current password verification: {current_user.check_password(current_password)}")
            
            if not current_user.check_password(current_password):
                return jsonify({
                    'success': False,
                    'error': 'Current password is incorrect'
                }), 400  # Changed from 401 to 400
            
            current_user.set_password(new_password)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Password updated successfully'
            })
            
        except Exception as e:
            db.session.rollback()
            print(f"Password update error: {str(e)}")  # Debug line
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    return jsonify({'success': False, 'error': 'Invalid action'}), 400


