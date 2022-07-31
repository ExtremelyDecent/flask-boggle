from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "watercolor123454321"

boggle_game = Boggle()

@app.route("/")
def home_display():
    """Displays home board. And game/default values"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template("index.html", board=board, highscore=highscore, nplays = nplays)
