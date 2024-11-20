from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user, login_user, logout_user
from models.models import Product, Order, User, db
from utils.api_login import api_login_required, api_admin_required
import json

users_api = Blueprint('users_api', __name__)

@users_api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'You successfully loged in': 'success'}), 200
    else:
        return jsonify({'Incorrect username or password': 'error'}), 401
    
@users_api.route('/logout', methods=['GET'])
@api_login_required
def api_logout():
    logout_user()
    return jsonify({'You are logged out': 'success'}), 200