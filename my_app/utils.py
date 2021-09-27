from my_app.models import Category, Product
from my_app import app


def get_categories():
    return Category.query.all()


def get_products(kw=None, cate_id=None, page=1):
    q = Product.query

    if kw:
        q = q.filter(Product.name.contains(kw))

    if cate_id:
        q = q.filter(Product.category_id == cate_id)

    size = app.config["PAGE_SIZE"]
    start = (page - 1) * size
    end = start + size

    return q.all()[start:end]


def count_products():
    return Product.query.count()
