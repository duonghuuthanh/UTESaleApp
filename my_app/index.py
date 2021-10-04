import math

from flask import render_template, request, session, jsonify
from my_app import app, my_login
from my_app.models import User
from flask_login import login_user
import hashlib
from admin import *
import utils


@app.route("/")
def home():
    categories = utils.get_categories()
    products = utils.get_products(category_id=request.args.get("category_id"),
                                  kw=request.args.get("kw"),
                                  page=int(request.args.get("page", 1)))

    count = utils.count_products()
    size = app.config["PAGE_SIZE"]

    return render_template("home.html",
                           categories=categories,
                           products=products,
                           page_num=math.ceil(count/size))


@my_login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=['post'])
def login_exe():
    username = request.form.get("username")
    password = request.form.get("password")
    password = str(hashlib.md5(password.encode("utf-8")).digest())
    user = User.query.filter(User.username == username,
                             User.password == password).first()
    if user: # dang nhap thanh cong
        login_user(user)

    return redirect("/admin")


@app.route("/api/add-item-cart", methods=['post'])
def add_to_cart():
    cart = session.get("cart")
    if not cart:
        cart = {}

    data = request.json
    # import pdb
    # pdb.set_trace()
    product_id = str(data["product_id"])

    if product_id in cart: # san pham da tung bo vao gio
        p = cart[product_id]
        p['quantity'] = p['quantity'] + 1
    else: # san pham chua bo vao gio
        cart[product_id] = {
            "product_id": data["product_id"],
            "product_name": data["name"],
            "product_price": data["price"],
            "quantity": 1
        }

    session["cart"] = cart

    return jsonify(utils.cart_stats(cart))




@app.route('/upload', methods=['post'])
def upload():
    avatar = request.files.get("avatar")
    if avatar:
        avatar.save("%s/static/images/%s" % (app.root_path, avatar.filename))
        return "SUCCESSFUL"

    return "FAILED"


if __name__ == '__main__':
    app.run(debug=True)
