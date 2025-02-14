from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_phone = db.Column(db.String(20), unique=True, nullable=False)
    limit_amount = db.Column(db.Float, nullable=False)
    state = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<User {self.user_phone}, Limit: {self.limit_amount}>"


def get_date_time():
    return datetime.now()


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, default=get_date_time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Expense {self.category}, Amount: {self.amount}, User ID: {self.user_id}, Date: {self.date}>"