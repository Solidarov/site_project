import os
import dummy_data as dd # importing dummy data for home and cart pages
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import LoginManager
from dotenv import load_dotenv
from models.models import db, Feedback, Product, User


# ENVIRONMENT VARIABLES
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# INITIALISE
app = Flask(__name__, static_folder='resources')
app.config['SECRET_KEY'] = SECRET_KEY
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
@app.route("/")
@app.route("/shop")
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        new_feedback = Feedback(name=name, email=email, message=message)
        db.session.add(new_feedback)
        db.session.commit()

        flash("Your feedback was succesfully sent", "success")
        return redirect(url_for('feedback'))
    
    return render_template("feedback.html")

@app.route("/cart")
def cart():
    return render_template("cart.html", products=dd.cart_products, total_price=254.33)

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

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration is successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)