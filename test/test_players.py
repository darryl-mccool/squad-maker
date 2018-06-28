import players

from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch


TESTJSON = {
    "players": [
        {
            "_id": "123",
            "firstName": "Ben",
            "lastName": "Schreiber",
            "skills": [
                {
                   "type": "Shooting",
                    "rating": 50
                },
                {
                    "type": "Skating",
                    "rating": 50
                },
                {
                    "type": "Checking",
                    "rating": 50
                }
            ]
        },
        {
            "_id": "99",
            "firstName": "Wayne",
            "lastName": "Gretzky",
            "skills": [
                {
                    "type": "Shooting",
                    "rating": 99
                },
                {
                    "type": "Skating",
                    "rating": 99
                },
                {
                    "type": "Checking",
                    "rating": 99
                }
            ]
        }
    ]
}


class TestPlayer(TestCase):

    def testEquality(self):
        player1 = players.Player("123", "Ben Schreiber", 50, 50, 50)
        player2 = players.Player("123", "Ben Schreiber", 50, 50, 50)
        self.assertEqual(player1, player2)

    def testInequality(self):
        player1 = players.Player("123", "Ben Schreiber", 50, 50, 50)
        player2 = players.Player("99", "Wayne Gretzky", 99, 99, 99)
        self.assertNotEqual(player1, player2)

    def testInequality__oneAttribute(self):
        player1 = players.Player("123", "Ben Schreiber", 50, 50, 50)
        player2 = players.Player("124", "Ben Schreiber", 50, 50, 50)
        self.assertNotEqual(player1, player2)

    def testFromJSON(self):
        data = {"_id": "123", "firstName": "Ben", "lastName": "Schreiber",
                "skills": [{"type": "Skating", "rating": 50},
                           {"type": "Shooting", "rating": 50},
                           {"type": "Checking", "rating": 50}]}
        expectedPlayer = players.Player("123", "Ben Schreiber", 50, 50, 50)
        player = players.Player.fromJSON(data)
        self.assertEqual(player, expectedPlayer)


class TestGetSkillRating(TestCase):

    def testGetSkillRatingSkating(self):
        skillData = [{"type": "Skating", "rating": 50},
                     {"type": "Shooting", "rating": 60},
                     {"type": "Checking", "rating": 40}]
        skillType = "Skating"
        self.assertEqual(players.getSkillRating(skillData, skillType), 50)

    def testGetSkillRatingShooting(self):
        skillData = [{"type": "Skating", "rating": 50},
                     {"type": "Shooting", "rating": 60},
                     {"type": "Checking", "rating": 40}]
        skillType = "Shooting"
        self.assertEqual(players.getSkillRating(skillData, skillType), 60)

    def testGetSkillRatingChecking(self):
        skillData = [{"type": "Skating", "rating": 50},
                     {"type": "Shooting", "rating": 60},
                     {"type": "Checking", "rating": 40}]
        skillType = "Checking"
        self.assertEqual(players.getSkillRating(skillData, skillType), 40)

    def testGetSkillRatingInvalidOption(self):
        skillData = [{"type": "Skating", "rating": 50},
                     {"type": "Shooting", "rating": 60},
                     {"type": "Checking", "rating": 40}]
        skillType = "Fighting"
        with self.assertRaises(ValueError):
            players.getSkillRating(skillData, skillType)


class TestPlayerList(TestCase):
    player1 = players.Player("123", "Ben Schreiber", 50, 50, 50)
    player2 = players.Player("99", "Wayne Gretzky", 99, 99, 99)

    def testEquality(self):
        playerList1 = players.PlayerList([self.player1, self.player2])
        playerList2 = players.PlayerList([self.player1, self.player2])
        self.assertEqual(playerList1, playerList2)

    @patch("json.load", MagicMock(return_value=TESTJSON))
    def testFromJSON(self):
        expectedPlayerList = players.PlayerList([self.player1, self.player2])

        with patch("builtins.open", mock_open()) as mock_file:
            playerList = players.PlayerList.fromJSON("myJSONFile")

        self.assertEqual(playerList, expectedPlayerList)

    def testToHTML(self):
        playerList = players.PlayerList([self.player1, self.player2])
        expectedHTML = playerList.table.__html__()
        html = playerList.toHTML()

        self.assertEqual(html, expectedHTML)
