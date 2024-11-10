import os
import dummy_data as dd # importing dummy data for home and cart pages
from flask import Flask, render_template, url_for
from dotenv import load_dotenv


# ENVIRONMENT VARIABLES
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# INITIALISE
app = Flask(__name__, static_folder='resources')
app.config['SECRET_KEY'] = SECRET_KEY


# ROUTING
@app.route("/")
@app.route("/shop")
def home():
    return render_template('home.html', products=dd.products)

@app.route("/about")
def about():
    return render_template("about.html")

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