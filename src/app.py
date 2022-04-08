# pylint: disable= C0114, C0115, C0116, E1101
# The above is fine, but I'd prefer that the full names are used for less ambiguity (e.g. "missing-module-docstring")
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


@login_manager.user_loader
def load_user(id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(id))


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

    user = User.query.filter_by(email=users_email).first()
    if user is None:
        user = User(email=users_email, name=users_name, pic=picture)
        print("Adding a new user")
        # if not add them to db
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    print("Already a saved user")
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


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


@app.route("/teams")
def teams():
    return render_template("teams.html")


@app.route("/search_form", methods=["POST", "GET"])
def search():
    """
    This function reveives input name from search form. Calls API and gets image,
    id and moves list.
    """
    pokemon_name = request.form.get("search")
    pokemon = pokemon_name.lower()
    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon + "/")

    # checking to see that pokemon exists in API
    if response.status_code == 404:
        flash("That pokemon does not exist. Please try again!")
        return redirect(url_for("main"))

    else:
        data = response.json()
        headlines = {"name": "", "id": "", "image": "", "moves": [], "moves_id": []}
        headlines.update({"name": data["name"]})
        headlines.update({"id": data["id"]})
        headlines.update({"image": data["sprites"]["front_shiny"]})
        length_of_moves = len(data["moves"])
        list_of_moves = []
        list_of_moves_id = []
        for i in range(length_of_moves):
            list_of_moves.append(data["moves"][i]["move"]["name"])
            url = data["moves"][i]["move"]["url"]
            split_url = url.split("/")
            move_id = split_url[6]
            list_of_moves_id.append(move_id)
        headlines.update({"moves": list_of_moves})
        headlines.update({"moves_id": list_of_moves_id})
        return render_template(
            "search.html",
            headlines=headlines,
            pokemon_name=pokemon,
            length=length_of_moves,
        )


@app.route("/add_pokemon_to_team/<id>", methods=["POST", "GET"])
def add_pokemon_to_team(id):
    pokemon = Pokemon(species_no=id, owner=current_user.id)
    db.session.add(pokemon)
    team = Team.query.filter_by(owner=current_user.id).first()
    add_pokemon = TeamHasPokemon(team=team.id, pokemon=pokemon.id)
    db.session.add(add_pokemon)
    db.session.commit()
    return render_template("teams.html")


@app.route("/create_team", methods=["POST"])
def create_team():
    team = Team(name="My Team", owner=current_user.id)
    print(team.owner)
    db.session.add(team)
    db.session.commit()

    return render_template("teams.html")


# Use this when testing locally
# The app.run I was using to test google authorization
if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)  # for deployment
    # app.run(ssl_context="adhoc", debug=True)  # for local use only
