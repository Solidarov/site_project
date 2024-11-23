from flask import (render_template, 
                   url_for, 
                   flash, 
                   redirect, 
                   request, 
                   Blueprint)

from flask_login import login_required, current_user
from models.models import db, Order, Feedback, Cart, Product
import json

shop_bp = Blueprint('shop', __name__)


@shop_bp.route("/")
@shop_bp.route("/shop")
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)


@shop_bp.route("/feedback", methods=['GET', 'POST'])
def feedback():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        new_feedback = Feedback(name=name, email=email, message=message)
        db.session.add(new_feedback)
        db.session.commit()

        flash("Your feedback was succesfully sent", "success")
        return redirect(url_for('shop.feedback'))
    
    return render_template("feedback.html")


@shop_bp.route("/cart")
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
    products, total_price = Cart.get_products_n_price(cart_items)

    return render_template('cart.html', products=products, total_price=total_price)


@shop_bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('shop.shop'))

    existing_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash("Product has been added to your cart.", "success")
    return redirect(url_for('shop.cart'))


@shop_bp.route('/checkout', methods=['POST', 'GET'])
@login_required
def checkout():
    if request.method == 'GET':
        return redirect(url_for('shop.cart'))

    email = request.form['email']
    address = request.form['address']
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Your cart is empty!", "danger")
        return redirect(url_for('shop.cart'))

    products, total_price = Cart.get_products_n_price(cart_items)

    order = Order(
        user_id=current_user.id,
        products=json.dumps(products),
        total_price=total_price,
        address=address,
        email=email
    )
    db.session.add(order)

    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    flash("Your order is accepted!", "success")
    return redirect(url_for('shop.home'))
    

@shop_bp.route("/about")
def about():
    return render_template("about.html")