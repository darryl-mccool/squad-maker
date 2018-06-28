from flask import Flask, render_template

from players import PlayerList

app = Flask(__name__)


@app.route("/")
def main():
    """
    Default page for webpage, which loads player data from a JSON file,
    and outputs them to a waiting list, which is displayed on the page.
    """
    playerList = PlayerList.fromJSON()

    return render_template('index.html', waitingList=playerList.toHTML())


if __name__ == "__main__":
    """
    When calling this file in the command line, run the application
    """
    app.run()
