from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

auth = Blueprint("auth", __name__)

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("Logged in!", category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Wrong Credentials', category='error')
            else:
                flash('Account Doesn\'t Exists', category='warning')

        return render_template("login.html",user=current_user)
    else:
        flash('Already Logged In', category='warning')
        return redirect(url_for('views.home'))


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            email = request.form.get("email")
            username = request.form.get("username")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            

            email_exists = User.query.filter_by(email=email).first()
            username_exists = User.query.filter_by(username=username).first()

            
            if email_exists:
                flash('Email is already in use.', category='error')
            elif username_exists:
                flash('Username is already in use.', category='error')
            elif password1 != password2:
                flash('Both The Password Dont Match', category='error')
            elif len(username) < 4:
                flash('Username Not Entered or Too Short , Minimum 4 Character', category='warning')
            elif len(password1) < 6:
                flash('Password Not Entered or Too Short , Minimum 4 Character', category='error')
            elif len(email) < 6:
                flash("Email Not Entered or Too Short", category='error')
            else:
                new_user = User(email=email, username=username,password=generate_password_hash(
                    password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash(f'Account Successfully Created , Welcome {username}',category="success")
                return redirect(url_for('views.home'))
                

        return render_template("signup.html",user=current_user,re=re)
    else:
        flash('Logout First', category='warning')
        return redirect(url_for('views.home'))


@auth.route("/logout")
def logout():
    if not current_user.is_authenticated:
        flash("Already Logged Out",category="warning")
    else:
        logout_user()
        flash("Logged Out Successfully",category="success")
    
    return redirect(url_for("auth.login"))