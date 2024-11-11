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
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    products = []
    total_price = 0

    for item in cart_items:
        product = Product.query.get(item.product_id)
        products.append({
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'quantity': item.quantity,
            'total': product.price * item.quantity,
            'id': item.id
        })
        total_price += product.price * item.quantity

    return render_template('cart.html', products=products, total_price=total_price)

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('shop'))

    existing_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash("Product has been added to your cart.", "success")
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST', 'GET'])
@login_required
def checkout():
    if request.method == 'GET':
        return redirect(url_for('cart'))

    address = request.form['address']
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Your cart is empty!", "danger")
        return redirect(url_for('cart'))

    products = []
    total_price = 0
    for item in cart_items:
        product = Product.query.get(item.product_id)
        products.append({
            'title': product.title,
            'quantity': item.quantity,
            'price': product.price,
            'total': product.price * item.quantity
        })
        total_price += product.price * item.quantity

    order = Order(
        user_id=current_user.id,
        products=json.dumps(products),
        total_price=total_price,
        address=address
    )
    db.session.add(order)

    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    flash("Your order is accepted!", "success")
    return redirect(url_for('home'))


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

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("You have successfully logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash("Incorrect username or password", "danger")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)