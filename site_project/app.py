import os
import dummy_data as dd # importing dummy data for home and cart pages
from flask import Flask, render_template, url_for, request, flash, redirect
from dotenv import load_dotenv
from models.models import db, Feedback


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


# ROUTING
@app.route("/")
@app.route("/shop")
def home():
    return render_template('home.html', products=dd.products)

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

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)