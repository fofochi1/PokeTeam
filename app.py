# pylint: disable= C0114, C0115, C0116, E1101
# The above is fine, but I'd prefer that the full names are used for less ambiguity (e.g. "missing-module-docstring")
# I'd also like for us to have justifications regarding the warnings we disable

from os import getenv

import flask

# Just for testing deployment; I used a separate file to fetch all env variables and imported them in other files for convenience
HOST = getenv("IP", "0.0.0.0")
PORT = int(getenv("PORT", "8080"))

app = flask.Flask(__name__)


@app.route("/")
def main():
    return flask.render_template("index.html")


app.run(debug=True, host=HOST, port=PORT)
