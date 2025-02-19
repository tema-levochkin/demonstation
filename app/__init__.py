from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(import_name=__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
database = SQLAlchemy(app)

from app import routers