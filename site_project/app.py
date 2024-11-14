from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.models import db, Feedback, Product, User, Cart, Order
from dotenv import load_dotenv
import json
import os


# ENVIRONMENT VARIABLES
load_dotenv()

# INITIALISE
app = Flask(__name__, static_folder='resources')
app.secret_key = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ROUTING
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("This user already exists.", "danger")
            return redirect(url_for('register'))
        
        is_admin = True if 'admin' in username.lower() else False

        new_user = User(username=username, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration is successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for('shop.home'))


from routes.admin import admin_bp
from routes.shop import shop_bp

app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)

if __name__ == "__main__":
    app.run(debug=True)