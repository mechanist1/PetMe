from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    posts = db.relationship('Form',lazy=True)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namepet = db.Column(db.String(150), nullable=False)
    favmeal = db.Column(db.String(150),nullable=False)
    Medic = db.Column(db.String(150),nullable=False)
    Gender = db.Column(db.String(150))
    Contact = db.Column(db.String(150))
    img =  db.Column(db.String(20), nullable=False, default='default.jpg')
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Form('{self.namepet}', '{self.date}')"

    


