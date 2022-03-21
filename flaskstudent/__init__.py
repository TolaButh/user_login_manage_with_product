from enum import unique
import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.utils import redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentdb.db'
app.config['SECRET_KEY']=b'tola1221'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
from flaskstudent import routes

