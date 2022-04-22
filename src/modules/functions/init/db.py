# pylint: disable = missing-function-docstring, relative-beyond-top-level, undefined-variable, wildcard-import
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
relative-beyond-top-level: pylint doesn't seem to like relative imports
undefined-variable: vars (db, etc.) are defined, hidden by wildcard
wildcard-import: convenient (programmatic imports instead of static)
"""

### IMPORTS
# native
from ...data.models import *


def init_db(app):
    db.init_app(app)
    # have to figure out where to import db from
    with app.app_context():
        db.create_all()
