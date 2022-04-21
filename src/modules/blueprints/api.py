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


@api_blueprint.route("/add_user_if_not_exists/<email>/<redirect_url>")
def add_user_if_not_exists(email, redirect_url):
    # email = args["email"]
    # redirect_url = args["redirect_url"]
    user = User.query.filter_by(email=email).first()
    if user is None:
        pass

    return redirect(url_for(redirect_url))


@api_blueprint.route("/search_pokemon")
def search_pokemon(pokemon):
    return get_pokemon_data(pokemon.lower())


# all database/API-calling routes belong here
