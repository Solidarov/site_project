from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required
from models.models import User, db

users_bp = Blueprint('users', __name__)

@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('users.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("This user already exists.", "danger")
            return redirect(url_for('users.register'))
        
        is_admin = True if 'admin' in username.lower() else False

        new_user = User(username=username, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration is successful! You can now log in.", "success")
        return redirect(url_for('users.login'))

    return render_template('register.html')


@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("You have successfully logged in!", "success")
            return redirect(url_for('shop.home'))
        else:
            flash("Incorrect username or password", "danger")

    return render_template('login.html')


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for('shop.home'))

