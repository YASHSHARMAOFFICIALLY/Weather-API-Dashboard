from flask import render_template, Blueprint, redirect, flash, request, url_for
from flask_login import login_required, logout_user, login_user
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import users
auth_bp = Blueprint('auth', __name__,url_prefix="/auth")
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        existing_username = users.query.filter_by(username=username).first()
        if existing_username:
            flash("Username already exists, please try another username")
            return redirect(url_for("auth.register"))
        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("auth.register"))
        new_user = users(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login", 'success')
        return redirect(url_for("auth.login"))
    return render_template("register.html")
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Logged in successfully", "success")
            return redirect(url_for("table.dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for("auth.login"))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
               
              
        



        
        
        
         

                        

