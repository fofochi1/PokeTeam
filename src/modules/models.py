# pylint: disable = missing-class-docstring, no-member
"""
Disabled Pylint Warnings & Justifications:
missing-class-docstring: unnecessary, classes are already straightforward
no-member: pylint doesn't seem to like "db.*"
"""


from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# since the models are in a separate file, they should be imported, along with db
# from app import db

db = SQLAlchemy()


# enforcing some naming conventions/standards

# having "DB" in the name of the table is misleading, as both a class and a table
class User(UserMixin, db.Model):
    __tablename__ = "User"
    # primary key should be an integer for auto-increment; changed the name to remove redundancy
    id = db.Column(db.Integer, primary_key=True)
    # changed email max length in accordance with Gmail's (6-30 character username)
    # since users can only log in with Google, storing "@gmail.com" is unnecessary
    email = db.Column(db.String(30))
    # do we really need to store names? we could just use the google username
    name = db.Column(db.String(100))
    pic = db.Column(db.String(120))

    def __repr__(self):
        return f"<User_id = {self.user_id}, Email = {self.email}, Name = {self.name}, Pic = {self.pic}>"

    # these functions are predefined by the UserMixin class that's being inherited
    # def get_id(self):
    #     """Return the id from the username."""
    #     return self.user_id

    # def is_active(self):
    #     """True, as all users are active."""
    #     return True


# team attributes:
# owner
# 6 Pokemon (could be stored as a list or as separate fields; I like list better since it's more natural, maybe comma separated?)
# anything else?
class Team(db.Model):
    __tablename__ = "Team"
    id = db.Column(db.Integer, primary_key=True)
    # user ID
    owner = db.Column(db.Integer)


# *** IMPORTANT ***
# should TrainerCard be its own class? or should it be merged with Team since they're basically the same thing?


# pokemon attributes:
# species
# ability
# moveset (same thing as for Team.pokemon: 4 moves, should probably be list)
# owner? doing so will allow users to re-use one particular Pokemon for multiple teams
# anything else?
class Pokemon(db.Model):
    __tablename__ = "Pokemon"
    id = db.Column(db.Integer, primary_key=True)
    # decisions to be made: should we have separate tables for species, abilities, moves, etc? The use is that we can use integer IDs instead of strings for these fields
    # using strings for now
    # species ID could be national dex number, for example
    species = db.Column(db.String(20))
    ability = db.Column(db.String(20))

