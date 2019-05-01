from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from machala_movie_mailer.private_variables import db_address

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_ADDRESS']
app.config['SQLALCHEMY_DATABASE_URI'] = db_address
db = SQLAlchemy(app)

from flask_movie_mailer import routes
