import math

from flask import render_template, request, redirect
from my_app import app, my_login
from my_app.models import User
from flask_login import login_user
import hashlib
from admin import *
import utils


@app.route("/")
def home():
    categories = utils.get_categories()
    products = utils.get_products(cate_id=request.args.get("category_id"),
                                  kw=request.args.get("kw"),
                                  page=int(request.args.get("page", 1)))

    return render_template("home.html",
                           categories=categories,
                           products=products,
                           page_number=math.ceil(utils.count_products()/app.config['PAGE_SIZE']))


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

@app.route('/upload', methods=['post'])
def upload():
    avatar = request.files.get("avatar")
    if avatar:
        avatar.save("%s/static/images/%s" % (app.root_path, avatar.filename))
        return "SUCCESSFUL"

    return "FAILED"



if __name__ == '__main__':
    app.run(debug=True)
