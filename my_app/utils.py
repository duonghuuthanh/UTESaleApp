from my_app.models import Category, Product
from my_app import app


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