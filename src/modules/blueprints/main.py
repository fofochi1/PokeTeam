# pylint: disable = missing-function-docstring, relative-beyond-top-level
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
relative-beyond-top-level: pylint doesn't seem to like relative imports
"""


### IMPORTS
# third-party
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

# native
from ..functions.external_apis.pokeapi import get_pokemon_data


main_blueprint = Blueprint("main", __name__)


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

    return render_template("search.html", pokemon_data=pokemon_data)
