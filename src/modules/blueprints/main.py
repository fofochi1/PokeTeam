# pylint: disable = missing-function-docstring
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
"""


### IMPORTS
# third-party
from flask import Blueprint, render_template
from flask_login import login_required


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/main")
@login_required
def main():
    return render_template("index.html")
