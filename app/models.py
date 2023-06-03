from flask_login import UserMixin
from app import db, login


@login.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    adr = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    bdate = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    pwd = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email
