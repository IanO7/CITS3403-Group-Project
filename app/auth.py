# app/auth.py
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from werkzeug.security import check_password_hash
from flask_dance.contrib.google import google
from .models import User
from . import db

auth = Blueprint("auth", __name__)

# ───────────── LOGIN (HTML FORM) ─────────────
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").lower()
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            flash("Logged in successfully.", "success")
            return redirect(url_for("views.profile"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


# ───────────── AJAX LOGIN ENDPOINT (optional) ─────────────
@auth.route("/api/login/email", methods=["POST"])
def api_email_login():
    data = request.get_json(silent=True) or {}
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify(success=False, message="Email and password required"), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        session["user_id"] = user.id
        return jsonify(success=True, message="Logged in"), 200

    return jsonify(success=False, message="Invalid credentials"), 401


# ───────────── GOOGLE CALLBACK (only fires on error) ─────────────
@auth.route("/login/google/authorized")
def google_authorized_error():
    # Should rarely hit this route—success handled by oauth_authorized signal
    flash("Google login failed.", "danger")
    return redirect(url_for("auth.login"))


# ───────────── SIGN‑UP ─────────────
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username        = request.form.get("username")
        email           = request.form.get("email", "").lower()
        password        = request.form.get("password")
        confirm_pass    = request.form.get("confirm_password")

        if password != confirm_pass:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")

        if User.query.filter_by(email=email).first():
            flash("That email is already registered.", "warning")
            return render_template("signup.html")

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        flash(f"Welcome, {username}! Account created.", "success")
        return redirect(url_for("views.profile"))

    return render_template("signup.html")


# ───────────── LOG‑OUT ─────────────
@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
