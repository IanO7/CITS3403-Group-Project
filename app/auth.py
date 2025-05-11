from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, current_app
)
from .models import User
from . import db
from werkzeug.utils import secure_filename
import os

 


auth = Blueprint('auth', __name__)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
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
