from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, current_app, jsonify
)
from .models import User
from . import db
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
from flask_login import login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        image_file = request.files.get('profileImage')
        image_filename = None

        if image_file:
            image_file = request.files.get('profileImage')
            image_filename = None
            
            filename = secure_filename(os.path.basename(image_file.filename))
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image_file.save(image_path)
            image_filename = filename


        username        = request.form.get('username')
        email           = request.form.get('email')
        password        = request.form.get('password')
        confirm_pass    = request.form.get('confirm_password')

        # 1) Passwords match?
        if password != confirm_pass:
            flash('Passwords do not match.', 'danger')
            return render_template('sign_up.html')

        # 2) Email unique?
        if User.query.filter_by(email=email).first():
            flash('That email is already registered.', 'warning')
            return render_template('sign_up.html')

        # 3) Create & login
        
        new_user = User(username=username, email=email, profileImage=image_filename)

  
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        flash(f'Welcome, {username}! Your account has been created.', 'success')
        return redirect(url_for('views.profile'))

    # GET
    return render_template('sign_up.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            return render_template('login.html')

        session['user_id'] = user.id
        flash('Logged in successfully.', 'success')
        return redirect(url_for('views.profile'))

    # GET
    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/verify_password', methods=['POST'])
@login_required
def verify_password():
    data = request.get_json()
    current_password = data.get('current_password')
    
    if check_password_hash(current_user.password_hash, current_password):
        return jsonify({'valid': True})
    return jsonify({'valid': False})


@auth.route('/settings', methods=['POST'])
@login_required
def update_settings():
    if request.form.get('action') == 'update_password':
        current_password = request.form.get('current-password')
        new_password = request.form.get('new-password')
        
        # Verify current password
        if not check_password_hash(current_user.password_hash, current_password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('settings'))
        
        # Update password
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash('Password updated successfully', 'success')
        
    return redirect(url_for('settings'))


