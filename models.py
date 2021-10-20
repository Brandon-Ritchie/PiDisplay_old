from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class DisplayEntry(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary key column, automatically generated IDs
    day_of_the_week = db.Column(
        db.String(15), index=True, unique=True
    )  # Day of the week for the entry
    start_time = db.Column(
        db.String(10), index=True, unique=False
    )  # Time for display to turn on
    switch_time = db.Column(
        db.String(10), index=True, unique=False
    )  # Time for display to switch slides
    end_time = db.Column(
        db.String(10), index=True, unique=False
    )  # time for display to turn off
    start_link_text = db.Column(
        db.String(30), index=True, unique=False
    )  # Display link text for first slide
    switch_link_text = db.Column(
        db.String(30), index=True, unique=False
    )  # Display link text for second slide


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
