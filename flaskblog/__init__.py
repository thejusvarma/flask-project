from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '48c92cc12c8608d0ae64d2615acf501a'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#  creating instance of database
db = SQLAlchemy(app)

# creating instance of bcryptused for encoding and decoding
bcrypt = Bcrypt(app)

# creating instance of login manager 
login_manager = LoginManager(app)

from flaskblog import routes