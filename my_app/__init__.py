from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12345678@localhost/utesaleapp?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "!@#$%^&*()(*&^%$#@#$%^&*("
app.config["PAGE_SIZE"] = 6
app.config["CLOUDINARY_INFO"] = {
    "cloud_name": "dxxwcby8l",
    "api_key": "448651448423589",
    "api_secret": "ftGud0r1TTqp0CGp5tjwNmkAm-A"
}
cloudinary.config(cloud_name=app.config["CLOUDINARY_INFO"]['cloud_name'],
                                      api_key=app.config["CLOUDINARY_INFO"]['api_key'],
                                      api_secret=app.config["CLOUDINARY_INFO"]['api_secret'])


db = SQLAlchemy(app=app)
my_login = LoginManager(app=app)
CART_KEY = "cart"
