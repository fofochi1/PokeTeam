# pylint: disable = missing-function-docstring, no-member, unused-wildcard-import, wildcard-import
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary (maybe for polishing phase)
no-member: pylint doesn't seem to like "db.*"
unused-wildcard-import: the imports are being used, just not explicitly
wildcard-import: using the wildcard is convenient
(main file doesn't change even if models file does)
"""

# I'd also like for us to have justifications regarding the warnings we disable
# Python standard libraries
from os import environ, urandom

import json

import requests


# Third party libraries
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user
from oauthlib.oauth2 import WebApplicationClient
from modules.data.env import DATABASE_URL, GOOGLE_CLIENT_ID, HOST, PORT
from modules.data.models import *


app = Flask(__name__)

# initialize items needed for flask-login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = urandom(16)

db.init_app(app)
with app.app_context():
    db.create_all()


def get_pokemon_url(name):
    """
    Creates url for API call
    """
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    url = base_url + name + "/"
    return url


def check_api_status_call(response):
    code = response.status_code
    return code


def is_user_in_db(useremail):
    user = User.query.filter_by(email=useremail).first()
    if user:
        return True
    return False


@app.route("/teams", methods=["GET", "POST"])
def teams():
    data = {"team": None, "pokemon_list": None}
    team = Team.query.filter_by(owner=current_user.id).first()
    pokemon_list = None
    if team is not None:

        def mapper(entry):
            pokemon = entry[0]
            response = requests.get(
                f"https://pokeapi.co/api/v2/pokemon/{pokemon.species_no}"
            ).json()
            setattr(pokemon, "image", response["sprites"]["front_default"])
            return pokemon

        query_result = (
            db.session.query(Pokemon, TeamHasPokemon)
            .filter(TeamHasPokemon.team == team.id)
            .filter(TeamHasPokemon.pokemon == Pokemon.id)
            .all()
        )
        pokemon_list = list(map(mapper, query_result))

    data["team"] = team
    data["pokemon_list"] = pokemon_list
    return render_template(
        "teams.html",
        data=data,
        user_name=current_user.name,
        user_email=current_user.email,
        user_pic=current_user.pic,
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    This function reveives input name from search form. Calls API and gets image,
    id and moves list.
    """
    data = None
    if request.method == "POST":
        search_term = request.form["search_term"].lower()
        url = get_pokemon_url(search_term)
        response = requests.get(url)
        if response.status_code == 404:
            flash("A Pokemon with that name (or ID) could not be found.")
            return redirect(url_for("search"))
        response = response.json()

        def mapper(move_wrapper):
            move_wrapper = move_wrapper["move"]
            move = {
                "name": move_wrapper["name"],
                "id": move_wrapper["url"].split("/")[-2],
            }
            return move

        data = {
            "name": response["name"],
            "species_no": response["id"],
            "image": response["sprites"]["front_default"],
            "moves": list(map(mapper, response["moves"])),
        }

    return render_template(
        "search.html",
        data=data,
        user_name=current_user.name,
        user_email=current_user.email,
        user_pic=current_user.pic,
    )


@app.route("/add_pokemon/<species_no>", methods=["POST"])
def add_pokemon(species_no):
    pokemon = Pokemon(species_no=species_no, owner=current_user.id)

    db.session.add(pokemon)
    team = Team.query.filter_by(owner=current_user.id).first()
    team_pokemon_record = TeamHasPokemon(team=team.id, pokemon=pokemon.id)
    db.session.add(team_pokemon_record)
    db.session.commit()
    return redirect(url_for("teams"))


@app.route("/create_team", methods=["POST"])
def create_team():
    team = Team(name="My Team", owner=current_user.id)
    db.session.add(team)
    db.session.commit()
    return redirect(url_for("teams"))


if __name__ == "__main__":
    # app.run(host=HOST, port=PORT)  # for deployment
    app.run(debug=True, host=HOST, port=PORT, ssl_context="adhoc")  # for local use only
