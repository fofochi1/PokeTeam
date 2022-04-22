# pylint: disable = missing-function-docstring, relative-beyond-top-level
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
relative-beyond-top-level: pylint doesn't like relative imports
"""

from ...blueprints.api import api_blueprint
from ...blueprints.index import index_blueprint
from ...blueprints.login import login_blueprint
from ...blueprints.main import main_blueprint


def get_blueprints():
    blueprints = [api_blueprint, index_blueprint, login_blueprint, main_blueprint]
    return blueprints
