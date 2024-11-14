from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """Хешує пароль і зберігає його."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Перевіряє, чи співпадає пароль з хешем."""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def access_denied():
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('shop.home'))


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, title, description, image, price):
        self.title = title
        self.description = description
        self.image = image
        self.price = price

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    products = db.Column(db.Text, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='New')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    
    def update_status(self, new_status):
        order = Order.query.get(self.id)
        order.status = new_status
        db.session.commit()


    @staticmethod
    def order_not_found(redir_page):
        flash("Order not found.", "danger")
        return redirect(url_for(redir_page))

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())


    @staticmethod
    def feedback_not_found(redir_page):
        flash("Feedback not found.", "danger")
        return redirect(url_for(redir_page))
