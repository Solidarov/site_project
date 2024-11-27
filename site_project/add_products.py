from app import db, app
from models.models import Product

with app.app_context():
    db.create_all()

    product1 = Product(title="The Christmas Premium Box", description="Exclusive Christmas gift box with 50 pcs. mix chocolate bites", image="images/box.webp", price=19.99)
    product2 = Product(title="The Ultimate Box", description="Exclusive gift box with 80 pcs. mix chocolate bites", image="images/simple-box.webp", price=29.99)
    product3 = Product(title="Simply Rich Arnold protein bar", description="Caramel, peanuts, and dark chocolate", image="images/protein.webp", price=10.00)
    product4 = Product(title="Simply Crispy Carrie - Cube with bites", description="Crunchy caramel, sea salt and milk chocolate", image="images/cube.webp", price=10.35)
    product5 = Product(title="Water bottle", description="IN NATURE WE TRUST", image="images/bottle.webp", price=50)
    product6 = Product(title="Christmas calendar", description="Perfect for true fans", image="images/calendar.webp", price=99.99)


    db.session.add_all([product1, product2, product3, product4, product5, product6])
    db.session.commit()
    print("База даних створена, продукти додані!")
