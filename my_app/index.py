import math
from flask import render_template, request, session, jsonify, redirect
from my_app import app, my_login, CART_KEY
from my_app.models import User
from flask_login import login_user, logout_user
import hashlib
from admin import *
import utils
import cloudinary
import cloudinary.uploader


@app.route("/")
def home():
    products = utils.get_products(category_id=request.args.get("category_id"),
                                  kw=request.args.get("kw"),
                                  page=int(request.args.get("page", 1)))

    count = utils.count_products()
    size = app.config["PAGE_SIZE"]

    return render_template("home.html",
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


@app.route("/user-login", methods=['get', 'post'])
def normal_user_login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.encode("utf-8")).digest())
        user = User.query.filter(User.username == username,
                                 User.password == password).first()
        if user:  # dang nhap thanh cong
            login_user(user)
            return redirect(request.args.get("next", "/"))
        else:
            err_msg = "Username hoac password khong chinh xac!"

    return render_template("login_user.html", err_msg=err_msg)


@app.route("/user-logout")
def normal_user_logout():
    logout_user()

    return redirect("/user-login")


@app.route("/api/add-item-cart", methods=['post'])
def add_to_cart():
    cart = session.get(CART_KEY)
    if not cart:
        cart = {}

    data = request.json

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

    session[CART_KEY] = cart

    return jsonify(utils.cart_stats(cart))


@app.route("/api/update-cart-item", methods=['put'])
def update_cart_item():
    cart = session.get(CART_KEY)

    if cart:
        data = request.json
        try:
            product_id = str(data['product_id'])
            quantity = data['quantity']
        except IndexError | KeyError as ex:
            print(ex)
        else:
            if product_id in cart:
                p = cart[product_id]
                p['quantity'] = quantity

                session[CART_KEY] = cart

                return jsonify({
                    "error_code": 200,
                    "cart_stats": utils.cart_stats(cart)
                })

    return jsonify({
        "error_code": 404
    })


@app.route("/api/delete-cart-item/<product_id>", methods=['delete'])
def delete_cart_item(product_id):
    cart = session.get(CART_KEY)
    if cart:
        if product_id in cart:
            del cart[product_id]
            session[CART_KEY] = cart

            return jsonify({
                "error_code": 200,
                "cart_stats": utils.cart_stats(cart)
            })

    return jsonify({
        "error_code": 404
    })


@app.route('/api/pay', methods=['post'])
def pay():
    cart = session.get(CART_KEY)
    if cart:
        if utils.add_receipt(cart):
            del session[CART_KEY]

            return jsonify({
                "error_code": 200
            })

    return jsonify({
        "error_code": 404
    })


@app.route("/cart")
def cart():
    return render_template('cart.html')


@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        try:
            password = request.form["password"]
            confirm_password = request.form['confirm-password']
            if password.strip() == confirm_password.strip():
                avatar = request.files['avatar']

                data = request.form.copy()
                del data['confirm-password']

                if avatar:
                    info = cloudinary.uploader.upload(avatar)
                    data['avatar'] = info['secure_url']

                if utils.add_user(**data):
                    return redirect("/user-login")
                else:
                    err_msg = "Du lieu dau vao khong hop le!"
            else:
                err_msg = "Mat khau khong khop!"
        except:
            err_msg = "He thong dang co loi! Vui long quay lai sau!"

    return render_template('register.html', err_msg=err_msg)


@app.context_processor
def common_context():
    categories = utils.get_categories()
    cart_stats = utils.cart_stats(session.get(CART_KEY))

    return {
        "categories": categories,
        "cart_stats": cart_stats
    }

@app.route('/upload', methods=['post'])
def upload():
    avatar = request.files.get("avatar")
    if avatar:
        avatar.save("%s/static/images/%s" % (app.root_path, avatar.filename))
        return "SUCCESSFUL"

    return "FAILED"


if __name__ == '__main__':
    app.run(debug=True)
