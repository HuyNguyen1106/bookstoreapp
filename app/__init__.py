from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "\xf4S\xb5\x1b4X\x97\x85\xdc\xc8\x91[6\xd6w\xd0"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/bookstoredb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app,name="QUAN LY NHA SACH", template_mode="bootstrap3")

login = LoginManager(app=app)