from app import database as db


class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    registration_date = db.Column(db.DateTime, default=db.func.current_timestamp)