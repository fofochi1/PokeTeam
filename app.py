# pylint: disable= C0114, C0115, C0116, E1101
import flask

app = flask.Flask(__name__)


@app.route("/")
def main():
    return flask.render_template("index.html")


app.run(debug=True)
