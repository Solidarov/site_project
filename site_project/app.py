from flask import Flask
from flask_login import LoginManager
from models.models import db, User
from dotenv import load_dotenv
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
login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.users import users_bp

# API ROUTES
from api.shop import shop_api
from api.users import users_api

app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(users_bp)

# API ROUTES
app.register_blueprint(shop_api, url_prefix='/api/shop')
app.register_blueprint(users_api, url_prefix='/api/users')

if __name__ == "__main__":
    app.run(debug=True)