# pylint: disable = missing-function-docstring, redefined-outer-name, unused-wildcard-import, wildcard-import
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
redefined-outer-name: being able to re-use parameter names is convenient
unused-wildcard-import: the imports are being used, just not explicitly
wildcard-import: using the wildcard is convenient (no need to change main file)
"""


### IMPORTS
## standard
from os import environ

## third-party
from flask import Flask

## native
# data
from .modules.data.env import APP_SECRET_KEY, DATABASE_URL, HOST, PORT

# functions
from .modules.functions.init.blueprints import get_blueprints
from .modules.functions.init.db import init_db
from .modules.functions.init.login_manager import init_login_manager


### FUNCTIONS
def create_app():
    app = Flask(__name__, static_folder="../client/build", static_url_path="")
    app.config["SECRET_KEY"] = APP_SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # disable warnings
    blueprints = get_blueprints()
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app


### MAIN PROCEDURE
if __name__ == "__main__":
    environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # what does this do?
    app = create_app()
    init_db(app)
    init_login_manager(app)
    # app.run(debug=True, host=HOST, port=PORT, ssl_context="adhoc")  # development
    app.run(host=HOST, port=PORT)  # production


# @app.route("/teams", methods=["GET", "POST"])
# def teams():
#     data = {"team": None, "pokemon_list": None}
#     team = Team.query.filter_by(owner=current_user.id).first()
#     pokemon_list = None
#     if team is not None:

#         def mapper(entry):
#             pokemon = entry[0]
#             response = requests.get(
#                 f"https://pokeapi.co/api/v2/pokemon/{pokemon.species_no}"
#             ).json()
#             setattr(pokemon, "image", response["sprites"]["front_default"])
#             return pokemon

#         query_result = (
#             db.session.query(Pokemon, TeamHasPokemon)
#             .filter(TeamHasPokemon.team == team.id)
#             .filter(TeamHasPokemon.pokemon == Pokemon.id)
#             .all()
#         )
#         pokemon_list = list(map(mapper, query_result))

#     data["team"] = team
#     data["pokemon_list"] = pokemon_list
#     return render_template(
#         "teams.html",
#         data=data,
#         user_name=current_user.name,
#         user_email=current_user.email,
#         user_pic=current_user.pic,
#     )
