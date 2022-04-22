# pylint: disable = missing-function-docstring, relative-beyond-top-level, undefined-variable, wildcard-import
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
undefined-variable: vars (db, etc.) are defined, hidden by wildcard
wildcard-import: convenient (programmatic imports instead of static)
"""


### IMPORTS
# third-party
from flask import Blueprint, redirect, url_for
from flask_login import current_user

# native
from ..data.models import *


api_blueprint = Blueprint("api", __name__, url_prefix="/api")


@api_blueprint.route("/create_team", methods=["POST"])
def create_team():
    team = Team(name="My Team", owner=current_user.id)
    db.session.add(team)
    db.session.commit()
    return redirect(url_for("main.teams"))


@api_blueprint.route("/create_pokemon/<species_no>", methods=["POST"])
def create_pokemon(species_no):
    pokemon = Pokemon(species_no=species_no, owner=current_user.id)
    db.session.add(pokemon)
    team = Team.query.filter_by(owner=current_user.id).first()
    team_pokemon_record = TeamHasPokemon(team=team.id, pokemon=pokemon.id)
    db.session.add(team_pokemon_record)
    db.session.commit()
    return redirect(url_for("main.teams"))


@api_blueprint.route("/delete_pokemon/<_id>", methods=["POST"])
def delete_pokemon(_id):
    pokemon = Pokemon.query.get(_id)
    team = Team.query.filter_by(owner=current_user.id).first()

    if pokemon is not None and team is not None:
        team_pokemon_record = TeamHasPokemon.query.filter_by(
            team=team.id, pokemon=pokemon.id
        ).first()
        if team_pokemon_record is not None:
            db.session.delete(team_pokemon_record)
            db.session.commit()
            db.session.delete(pokemon)
            db.session.commit()

    return redirect(url_for("main.teams"))
