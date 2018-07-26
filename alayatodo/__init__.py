# -*- coding: utf-8 -*-
"""module file."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/alayatodo.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# app and db init
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)


import alayatodo.views  # noqa
