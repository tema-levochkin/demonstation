from datetime import datetime

from app import database as db


class Users(db.Model): 
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f"<User: {self.username}>"