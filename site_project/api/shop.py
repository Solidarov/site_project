from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user
from models.models import Product, Order, User,Feedback, db
from utils.api_login import api_login_required, api_admin_required
from email_validator import validate_email, EmailNotValidError
import json

shop_api = Blueprint('shop_api', __name__)

# Products
@shop_api.route('/products', methods=['GET'])
def get_products_api():
    try:
        products = Product.query.all()
        return jsonify(
            [{
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'image': product.image,
                'price': product.price,
            } 
            for product in products]
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@shop_api.route('/products/<int:product_id>', methods=['GET'])
def product_details_api(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "image": product.image,
            "price": product.price,
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@shop_api.route('/products', methods=['POST'])
@api_admin_required
def add_product_api():
    try:
        data = request.get_json()
        product = Product(
            title=data['title'],
            description=data['description'],
            image=data['image'],
            price=round(data['price'], 2)
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'Product added': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@shop_api.route('/products/<int:product_id>', methods=['DELETE'])
@api_admin_required
def delete_product_api(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({'Product deleted': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

# Feedback
@shop_api.route('/feedbacks', methods=['GET'])
@api_admin_required
def get_feedbacks_api():
    try:
        fedbacks = Feedback.query.all()
        if not fedbacks:
            return jsonify({'error': 'No feedbacks found'}), 404
        return jsonify(
                [{
                    "id": feedback.id,
                    "name": feedback.name,
                    "email": feedback.email,
                    "message": feedback.message,
                    "created_at": feedback.created_at
                } for feedback in fedbacks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@shop_api.route('/feedbacks/<int:feedback_id>', methods=['GET'])
@api_admin_required
def feedback_details_api(feedback_id):
    try:
        feedback = Feedback.query.get(feedback_id)

        if not feedback:
            return jsonify({'error': 'Feedback not found'}), 404
        
        return jsonify({
            "id": feedback.id,
            "name": feedback.name,
            "email": feedback.email,
            "message": feedback.message,
            "created_at": feedback.created_at
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
        

@shop_api.route('/feedbacks', methods=['POST'])
def add_feedback_api():
    try:
        data = request.get_json()
        
        #validate email
        email_check = validate_email(data['email'])
        f_email = email_check.normalized

        feedback = Feedback(
            name = data['name'],
            email = f_email,
            message = data['message']
        )

        db.session.add(feedback)
        db.session.commit()

        return jsonify({'Feedback added': 'success'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    except EmailNotValidError as e:
        return jsonify({'error': 'Email is not valid', 'message': str(e)}), 400
    

@shop_api.route('/feedbacks/<int:feedback_id>', methods=['DELETE'])
@api_admin_required
def delete_feedback_api(feedback_id):
    try:
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            return jsonify({'error': 'Feedback not found'}), 404
        db.session.delete(feedback)
        db.session.commit()
        return jsonify({'Feedback deleted': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

