import os
import dummy_data as dd # importing dummy data for home and cart pages
from flask import Flask, render_template, url_for
from dotenv import load_dotenv


# ENVIRONMENT VARIABLES
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# INITIALISE
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


# ROUTING
@app.route("/")
def home_page():
    return render_template('home.html', products=dd.products)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/cart")
def cart_page():
    return render_template("cart.html", cart_items=dd.cart_products)

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/sign-in")
def sign_in_page():
    return render_template("sign_in.html")


if __name__ == "__main__":
    app.run(debug=True)