# app/auth.py
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, current_app
)
from werkzeug.security import check_password_hash
#from flask_dance.contrib.google import google
from .models import User
from . import db
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        image_file = request.files.get('profileImage')
        image_filename = None

        if image_file:
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

        if password != confirm_pass:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")

        if User.query.filter_by(email=email).first():
            flash("That email is already registered.", "warning")
            return render_template("signup.html")

        # 3) Create & login
        new_user = User(username=username, email=email, profileImage=image_filename)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        flash(f"Welcome, {username}! Account created.", "success")
        return redirect(url_for("views.profile"))

    # GET
    return render_template('signup.html')


# ───────────── LOG‑OUT ─────────────
@auth.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


