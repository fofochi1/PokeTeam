# pylint: disable = missing-class-docstring, no-member
"""
Disabled Pylint Warnings & Justifications:
missing-class-docstring: unnecessary, classes are already straightforward
no-member: pylint doesn't seem to like "db.*"
"""


from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    # do we really need to store names/pics? we could just use the google username
    name = db.Column(db.String(100))
    pic = db.Column(db.String(120))

    def __repr__(self):
        return "<id = {self.id}, email = {self.email}, Name = {self.name}, Pic = {self.pic}>"

    def get_id(self):
        """Return the id from the username."""
        return self.id


class Team(db.Model):
    __tablename__ = "Team"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey("User.id"))

    name = db.Column(db.String(30))


class Pokemon(db.Model):
    __tablename__ = "Pokemon"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey("User.id"))

    ability = db.Column(db.Integer)
    species_no = db.Column(db.Integer)  # National Dex no.


# unneeded tables
# class Ability(db.Model):
#     __tablename__ = "Ability"
#     id = db.Column(db.Integer, primary_key=True)


# class Move(db.Model):
#     __tablename__ = "Move"
#     id = db.Column(db.Integer, primary_key=True)


# relationships (cross-referencing tables)
class PokemonHasMove(db.Model):
    __tablename__ = "PokemonHasMove"
    pokemon = db.Column(db.Integer, db.ForeignKey("Pokemon.id"), primary_key=True)
    move = db.Column(db.Integer, primary_key=True)


class TeamHasPokemon(db.Model):
    __tablename__ = "TeamHasPokemon"
    team = db.Column(db.Integer, db.ForeignKey("Team.id"), primary_key=True)
    pokemon = db.Column(db.Integer, db.ForeignKey("Pokemon.id"), primary_key=True)
