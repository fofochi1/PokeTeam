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


class User(UserMixin, db.Model):
    __tablename__ = "User"
    # primary key should be an integer for auto-increment; changed the name to remove redundancy
    # The primary key should be a float, an integer key is not able to store the google id# properly
    id = db.Column(db.Float, primary_key=True)
    # changed email max length in accordance with Gmail's (6-30 character username)
    # since users can only log in with Google, storing "@gmail.com" is unnecessary
    email = db.Column(db.String(30))
    # do we really need to store names? we could just use the google username
    name = db.Column(db.String(100))
    pic = db.Column(db.String(120))

    def __repr__(self):
        return "<id = {self.id}, email = {self.email}, Name = {self.name}, Pic = {self.pic}>"


class Team(db.Model):
    __tablename__ = "Team"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey("User.id"))

    name = db.Column(db.String(30))


class Pokemon(db.Model):
    __tablename__ = "Pokemon"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Float, db.ForeignKey("User.id"))

    ability = db.Column(db.Integer, db.ForeignKey("Ability.id"))
    species_no = db.Column(db.Integer)  # National Dex no.


class Ability(db.Model):
    __tablename__ = "Ability"
    id = db.Column(db.Integer, primary_key=True)


class Move(db.Model):
    __tablename__ = "Move"
    id = db.Column(db.Integer, primary_key=True)


# relationships (cross-referencing tables)
class PokemonHasMove(db.Model):
    __tablename__ = "PokemonHasMove"
    pokemon = db.Column(db.Integer, db.ForeignKey("Pokemon.id"), primary_key=True)
    move = db.Column(db.Integer, db.ForeignKey("Move.id"), primary_key=True)


class TeamHasPokemon(db.Model):
    __tablename__ = "TeamHasPokemon"
    team = db.Column(db.Integer, db.ForeignKey("Team.id"), primary_key=True)
    pokemon = db.Column(db.Integer, db.ForeignKey("Pokemon.id"), primary_key=True)
