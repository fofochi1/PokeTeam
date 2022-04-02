# pylint: disable = missing-class-docstring, no-member
"""
Disabled Pylint Warnings & Justifications:
missing-class-docstring: unnecessary, classes are already straightforward
no-member: pylint doesn't seem to like "db.*"
"""
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# from app import db

db = SQLAlchemy()


class UserDB(UserMixin, db.Model):
    __tablename__ = "UserDB"
    user_id = db.Column(db.Float, unique=True, primary_key=True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    pic = db.Column(db.String(120))

    def __repr__(self):
        return f"<User_id = {self.user_id}, Email = {self.email}, Name = {self.name}, Pic = {self.pic}>"

    def get_id(self):
        """Return the id from the username."""
        return self.user_id

    # def is_active(self):
    #     """True, as all users are active."""
    #     return True
