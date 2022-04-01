# pylint: disable= C0114, C0115, C0116, E1101
# The above is fine, but I'd prefer that the full names are used for less ambiguity (e.g. "missing-module-docstring")
# I'd also like for us to have justifications regarding the warnings we disable
# Python standard libraries
from os import environ, getenv, urandom

import json

import requests


# Third party libraries
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient

# Just for testing deployment; I used a separate file to fetch all env variables and imported them in other files for convenience
HOST = getenv("IP", "0.0.0.0")
PORT = int(getenv("PORT", "8080"))

load_dotenv(find_dotenv())

app = Flask(__name__)

# initialize items needed for flask-login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Configuration
GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = urandom(16)
# app.secret_key = environ.get("SECRET_KEY") or urandom(24)

db = SQLAlchemy(app)
from modules.models import *

db.create_all()


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return UserDB.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


@app.route("/")
def index():
    # will redirect the user to the appropriate page according to if they are logged in
    if current_user.is_authenticated:
        return redirect(url_for("main"))
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
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    newUser = UserDB(user_id=unique_id, email=users_email, name=users_name, pic=picture)
    if isUserInDB(unique_id) == False:
        # if not add them to db
        db.session.add(newUser)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(newUser)

    # Send user back to homepage
    return redirect(url_for("index"))


def isUserInDB(userID):
    result = db.session.query(UserDB.query.filter_by(user_id=userID).exists())
    # if we get a non-empty result from the DB, that means they already exist
    if result:
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


@app.route("/teams")
def teams():
    return render_template("teams.html")


@app.route("/search_form", methods=["POST"])
def search():
    pokemon_name = request.form.get("search")
    return render_template("search.html")


# app.run(debug=True, host=HOST, port=PORT)

# The app.run I was using to test google authorization
if __name__ == "__main__":
    app.run(ssl_context="adhoc")
