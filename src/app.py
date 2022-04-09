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
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from modules.data.env import (
    DATABASE_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_DISCOVERY_URL,
    HOST,
    PORT,
)
from modules.data.models import *


app = Flask(__name__)

# initialize items needed for flask-login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


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


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


@app.route("/")
def index():
    # will redirect the user to the appropriate page according to if they are logged in
    if current_user.is_authenticated:
        print("You may pass")
        return redirect(url_for("main"))
    print("You may not pass")
    return redirect(url_for("login"))


@app.route("/login_request")
def login_request():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login")
def login():
    print("Yay, logging in")
    return render_template("login.html")


@app.route("/login_request/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User(email=users_email, name=users_name, pic=picture)
    if not is_user_in_db(users_email):
        print("Adding a new user")
        # if not add them to db
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    print("Already a saved user")
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


def is_user_in_db(useremail):
    user = User.query.filter_by(email=useremail).first()
    if user:
        return True
    return False


@app.route("/logout")
@login_required
def logout():
    # logout the current user with flask login and redirect to main page
    logout_user()
    return redirect(url_for("index"))


@app.route("/main")
@login_required
def main():
    return render_template(
        "index.html",
        user_name=current_user.name,
        user_email=current_user.email,
        user_pic=current_user.pic,
    )


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
    return render_template("teams.html", data=data)


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

    return render_template("search.html", data=data)


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
    # app.run(debug=True, host=HOST, port=PORT)  # for deployment
    app.run(debug=True, ssl_context="adhoc")  # for local use only
