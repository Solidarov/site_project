# create_db.py
from app import db, app

with app.app_context():
    db.create_all()
    print("База даних створена!")