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

## native
# data
from ..data.models import *

# functions
from ..functions.external_apis.pokeapi import get_pokemon_data


api_blueprint = Blueprint("api", __name__, url_prefix="/api")


@api_blueprint.route("/oof")
def oof():
    print("Cringe")
    return "3"


@api_blueprint.route("/add_user_if_not_exists/<email>/<redirect_url>")
def add_user_if_not_exists(email, redirect_url):
    # email = args["email"]
    # redirect_url = args["redirect_url"]
    user = User.query.filter_by(email=email).first()
    if user is None:
        pass

    return redirect(url_for(redirect_url))


@api_blueprint.route("/create_team/<_id>", methods=["POST"])
def create_team(_id):
    team = Team(name="My Team", owner=_id)
    db.session.add(team)
    db.session.commit()
    return redirect(url_for("teams"))


@api_blueprint.route("/create_pokemon/<species_no>", methods=["POST"])
def create_pokemon(species_no):
    redirect_url = url_for("main.teams")
    pokemon = Pokemon(species_no=species_no, owner=current_user.id)

    db.session.add(pokemon)
    team = Team.query.filter_by(owner=current_user.id).first()
    team_pokemon_record = TeamHasPokemon(team=team.id, pokemon=pokemon.id)
    db.session.add(team_pokemon_record)
    db.session.commit()
    return redirect(redirect_url)


# all database/API-calling routes belong here
