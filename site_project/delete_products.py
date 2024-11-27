from app import db, app
from models.models import Product

with app.app_context():
    db.session.query(Product).delete()
    db.session.commit()
    print("Усі продукти успішно видалені!")
