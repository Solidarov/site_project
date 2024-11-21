from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user, login_user, logout_user
from models.models import Product, Order, User, db
from utils.api_login import api_login_required, api_admin_required
import json

users_api = Blueprint('users_api', __name__)

@users_api.route('/login', methods=['POST'])
def login_api():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            login_user(user)
            return jsonify({'You successfully loged in': 'success'}), 200
        else:
            return jsonify({'Incorrect username or password': 'error'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@users_api.route('/logout', methods=['GET'])
@api_login_required
def logout_api():
    try:
        logout_user()
        return jsonify({'You are logged out': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@users_api.route('/register', methods=['POST'])
def register_api():
    try:
        data = request.get_json()

        username = data['username']
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
                return jsonify({'error': 'Passwords don`t match'}), 400

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return jsonify({'error': 'User exist'}), 400
            
        is_admin = True if 'admin' in username.lower() else False

        new_user = User(username=username, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'User registered successfully': 'success', 'message': 'Now you can login'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@users_api.route('/users', methods=['GET'])
@api_admin_required
def show_users_api():
    try:
        users = User.query.all()
        if not users:
            return jsonify({'error': "No users"}), 404
        
        return jsonify(
            [{
                "id": user.id,
                'username': user.username,
                "is_admin": user.is_admin
            } for user in users]
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@users_api.route('/users/<int:user_id>', methods=['GET'])
@api_admin_required
def user_details_api(user_id):
    try:
        
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@users_api.route('/users/<int:user_id>', methods=['DELETE'])
@api_admin_required
def user_delete_api(user_id):
    try:
        
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"User successfully deleted": "success"}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400