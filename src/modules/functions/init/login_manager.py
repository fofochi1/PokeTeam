# pylint: disable = missing-function-docstring, relative-beyond-top-level
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
relative-beyond-top-level: pylint doesn't like relative imports
"""


### IMPORTS
# third-party
from flask_login import LoginManager

# native
from ...data.models import User


def init_login_manager(app):
    login_manager = LoginManager()

    @login_manager.user_loader
    def get_user(_id):
        return User.query.get(_id)

    @login_manager.unauthorized_handler
    def handle_unauthorized_user():
        return "You must be logged in to access this content.", 403

    login_manager.init_app(app)
