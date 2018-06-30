import json

from flask_table import Table, Col

# Default JSON Data file
JSONFILE = "players.json"

SKILLTYPES = ["Skating", "Shooting", "Checking"]


def getSkillRating(sklData, sklType):
    """
    Get the rating for a given skill from
    a single player's skill data

    Skills are expected to be in one of the predetermined
    skill categories
    """
    if sklType not in SKILLTYPES:
        raise ValueError("%s is not a valid skill")
    return [skl for skl in sklData if skl['type'] == sklType][0]['rating']


class Player:
    """Representation of a Hockey Player

    A Player contains a unique identifier, a name, and a series
    of skill ratings that correspond to the skill types at the
    head of the file.

    """
    def __init__(self, id, name,
                 skateRating, shootRating, checkRating):
        """
        Create a Player
        """
        self._id = id
        self.name = name
        self.skate = skateRating
        self.shoot = shootRating
        self.check = checkRating

    def __eq__(self, other):
        """
        Override the equality operator so that two players are
        only equal if all of their attributes are equal.
        """
        if isinstance(other, self.__class__):
            return (self._id == other._id and
                    self.name == other.name and
                    self.skate == other.skate and
                    self.shoot == other.shoot and
                    self.check == other.check)
        else:
            return False

    @classmethod
    def fromJSON(cls, data):
        """
        Create a Player from a JSON dictionary containing player information
        """
        return cls(data["_id"],
                   ' '.join([data["firstName"], data["lastName"]]),
                   getSkillRating(data["skills"], "Skating"),
                   getSkillRating(data["skills"], "Shooting"),
                   getSkillRating(data["skills"], "Checking"))


class PlayerList:
    """Representation of a set of players

    Allows players to be grouped together, and for them to
    be output in an HTML table for webpage viewing.

    """
    def __init__(self, players):
        """
        Create a PlayerList and generate a HTML table for itself
        """
        self.players = players
        self.updateTable()

    def updateTable(self):
        emptyMsg = "No Players on Waiting List"
        tableClasses = ["playerList"]
        tableHTMLAttrs = {"align": "center"}
        self.table = PlayerTable(self.players,
                                 classes=tableClasses,
                                 no_items=emptyMsg,
                                 html_attrs=tableHTMLAttrs)

    def toHTML(self):
        """
        Update and write out the HTML table corresponding to the list of
        players.

        Defaults to printing out to the HTML file for the Waiting List
        """
        self.updateTable()
        html = self.table.__html__()
        return html

    def __eq__(self, other):
        """
        Override the equality operator so that two PlayerLists are
        equal if their interal list of players are the same
        """
        if isinstance(other, self.__class__):
            return self.players == other.players
        else:
            return False

    @classmethod
    def fromJSON(cls, fn=JSONFILE):
        """
        Read data from a JSON file, and create a PlayerList from it

        Defaults to the provided example file, players.json
        """
        players = []
        with open(fn) as f:
            data = json.load(f)
        for player in data["players"]:
            p = Player.fromJSON(player)
            players.append(p)
        return cls(players)


class PlayerTable(Table):
    """

    HTML Table with columns for Player name and skills

    """
    name = Col("Name")
    skate = Col("Skating")
    shoot = Col("Shooting")
    check = Col("Checking")
