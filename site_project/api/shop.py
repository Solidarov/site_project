from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user
from models.models import Product, Order, User, Feedback, Cart, db
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
    

# Cart 
@shop_api.route('/cart', methods=['GET'])
@api_login_required
def get_user_cart_api():
    try:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 404
        
        products, total_price = Cart.get_products_n_price(cart_items)
        return jsonify({'products': products, 'total_price': total_price}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@shop_api.route('/cart', methods=['POST'])
@api_login_required
def add_to_cart_api():
    try:
        products = request.get_json()

        for product in products:
            product_id = product['product_id']
            product_quantity = product['quantity']

            product = Product.query.get(product_id)
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            existing_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

            if existing_item:
                existing_item.quantity += product_quantity
            else:
                cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=product_quantity)
                db.session.add(cart_item)

            db.session.commit()

        return jsonify({'Products added': 'success'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@shop_api.route('/cart', methods=['DELETE'])
@api_login_required
def delete_cart_api():
    try:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 404
        
        for item in cart_items:
            db.session.delete(item)
            db.session.commit()
        return jsonify({'Cart deleted': 'success'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Orders
@shop_api.route('/orders', methods=['GET'])
@api_admin_required
def get_all_orders():
    try:
        orders = Order.query.all()
        
        if not orders:
            return jsonify({"error": "Orders not found"}), 404
        
        return jsonify(
            [{
                'id': order.id,
                'user_id': order.user_id,
                'email': order.email,
                
                'products': 
                    [{
                        'title': product['title'],
                        'quantity': product['quantity'],
                        'price': product['price'],
                        'total': product['total']
                    } for product in json.loads(order.products)],
                
                'total_price': order.total_price,
                'address': order.address,
                'status': order.status,
                'created_at': order.created_at        
                } for order in orders]
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@shop_api.route('/orders/<int:order_id>', methods=['GET'])
@api_admin_required
def order_details_api(order_id):
    try:
        order = Order.query.get(order_id)

        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        return jsonify({

                    'id': order.id,
                    'user_id': order.user_id,
                    'email': order.email,
                    
                    'products': 
                        [{
                            'title': product['title'],
                            'quantity': product['quantity'],
                            'price': product['price'],
                            'total': product['total']
                        } for product in json.loads(order.products)],
                    
                    'total_price': order.total_price,
                    'address': order.address,
                    'status': order.status,
                    'created_at': order.created_at        
                })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@shop_api.route('/orders', methods=['POST'])
@api_login_required
def add_order_api():
    try:
        data = request.get_json()

        #validate email
        email_check = validate_email(data['email'])
        f_email = email_check.normalized

        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 404
        
        products, total_price = Cart.get_products_n_price(cart_items)

        order = Order(
            user_id=current_user.id,
            products=json.dumps(products),
            total_price=total_price,
            address=data['address'],
            email=f_email
        )
        db.session.add(order)

        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        return jsonify({'Order added': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@shop_api.route("/orders", methods=['DELETE'])
@api_admin_required
def delete_all_orders_api():
    try:
        orders = Order.query.all()
        if not orders:
            return jsonify({'error': 'Orders not found'}), 404
        
        for order in orders:
            db.session.delete(order)
            db.session.commit()

        return jsonify({'Orders deleted': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@shop_api.route("/orders/<int:order_id>", methods=['DELETE'])
@api_admin_required
def delete_order_by_id_api(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        db.session.delete(order)
        db.session.commit()
            
        return jsonify({'Order deleted': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@shop_api.route("/orders/<int:order_id>", methods=['PUT'])
@api_admin_required
def update_status_order(order_id):
    try:
        data = request.get_json()
        new_status = data['status'].capitalize()
        possible_status = ['New', 'In processing', 'Send', 'Delivered', 'Canceled']
        
        if new_status not in possible_status:
            return jsonify({'error': 'Invalid status'}), 400
        
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order.update_status(new_status)
        return jsonify({'Order status updated': 'success'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400