# pylint: disable = missing-function-docstring, relative-beyond-top-level
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
relative-beyond-top-level: pylint doesn't seem to like relative imports
"""


### IMPORTS
## third-party
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

## native
# data
from ..data.models import db, Pokemon, Team, TeamHasPokemon

# functions
from ..functions.external_apis.pokeapi import get_pokemon_data


main_blueprint = Blueprint("main", __name__, static_folder="../../static")


@main_blueprint.route("/main")
@login_required
def main():
    return render_template("index.html")


@main_blueprint.route("/search", methods=["GET", "POST"])
@login_required
def search():
    pokemon_data = None
    if request.method == "POST":
        pokemon = request.form["search_term"]
        pokemon_data, error = get_pokemon_data(pokemon)
        if error is not None:
            flash("A Pokemon with that name (or ID) could not be found.")
            return redirect(url_for("main.search"))

    query_result = (
        db.session.query(Pokemon, TeamHasPokemon)
        .filter(TeamHasPokemon.team == Team.id)
        .filter(TeamHasPokemon.pokemon == Pokemon.id)
        .all()
    )
    team_count = len(list(query_result))

    return render_template(
        "search.html", pokemon_data=pokemon_data, team_count=team_count
    )


@main_blueprint.route("/teams", methods=["GET", "POST"])
def teams():
    data = {"team": None, "pokemon_list": None}
    team = Team.query.filter_by(owner=current_user.id).first()
    pokemon_list = None
    if team is not None:

        def mapper(entry):
            pokemon = entry[0]
            pokemon_data, error = get_pokemon_data(str(pokemon.species_no))
            if error is not None:
                return "An error occurred", 400
            setattr(pokemon, "sprite", pokemon_data["sprite"])
            return pokemon

        query_result = (
            db.session.query(Pokemon, TeamHasPokemon)
            .filter(TeamHasPokemon.team == Team.id)
            .filter(TeamHasPokemon.pokemon == Pokemon.id)
            .all()
        )
        pokemon_list = list(map(mapper, query_result))

    data["team"] = team
    data["pokemon_list"] = pokemon_list
    return render_template("teams.html", data=data)
