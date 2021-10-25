from my_app.models import Category, Product, Receipt, ReceiptDetails, User
from my_app import app, db
from flask_login import current_user
import hashlib


def get_categories():
    return Category.query.all()


def get_products(kw=None, category_id=None, page=None):
    products = Product.query

    if kw:
        products = products.filter(Product.name.contains(kw))

    if category_id:
        products = products.filter(Product.category_id == category_id)

    if page:
        size = app.config["PAGE_SIZE"]
        start = (page - 1) * size
        end = start + size

        return products.all()[start:end]

    return products.all()


def count_products():
    return Product.query.count()


def add_receipt(cart):
    if cart:
        try:
            receipt = Receipt(user=current_user)
            db.session.add(receipt)

            for item in cart.values():
                detail = ReceiptDetails(receipt=receipt,
                                        product_id=item['product_id'],
                                        quantity=item['quantity'],
                                        unit_price=item['product_price'])
                db.session.add(detail)

            db.session.commit()

            return True
        except Exception as ex:
            print("RECEIPT ERROR: " + str(ex))

    return False


def cart_stats(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for p in cart.values():
            total_quantity += p["quantity"]
            total_amount += p["quantity"] * p["product_price"]

    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }


def add_user(name, username, password, avatar=None):
    password = str(hashlib.md5(password.encode("utf-8")).digest())
    user = User(name=name,
                username=username,
                password=password,
                avatar=avatar)
    db.session.add(user)

    try:
        db.session.commit()
        return True
    except:
        return False
