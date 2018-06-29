import squads

from unittest import TestCase
from unittest.mock import mock_open, patch

from players import Player, PlayerList, PlayerTable


class TestSquad(TestCase):
    player1 = Player("123", "Ben Schreiber", 51, 51, 51)
    player2 = Player("99", "Wayne Gretzky", 99, 99, 99)

    def testGetAveragePlayer(self):
        expectedAvg = (51+99)//2
        expectedAvgPlayer = Player(None, squads.AVERAGENAME, expectedAvg,
                                   expectedAvg, expectedAvg)

        squad = squads.Squad(1, [self.player1, self.player2])
        self.assertEqual(squad.getAveragePlayer(), expectedAvgPlayer)

    def testGetAveragePlayer__odd(self):
        player1 = Player("123", "Ben Schreiber", 50, 50, 50)
        player2 = Player("99", "Wayne Gretzky", 99, 99, 99)
        expectedAvg = (50+99)//2
        expectedAvgPlayer = Player(None, squads.AVERAGENAME, expectedAvg,
                                   expectedAvg, expectedAvg)

        squad = squads.Squad(1, [player1, player2])
        self.assertEqual(squad.getAveragePlayer(), expectedAvgPlayer)

    def testGetAveragePlayer__differentValues(self):
        player1 = Player("123", "Ben Schreiber", 50, 40, 30)
        player2 = Player("99", "Wayne Gretzky", 99, 98, 97)
        expectedAvgPlayer = Player(None, squads.AVERAGENAME, (50+99)//2,
                                   (40+98)//2, (30+97)//2)

        squad = squads.Squad(1, [player1, player2])
        self.assertEqual(squad.getAveragePlayer(), expectedAvgPlayer)

    def testToHTML(self):
        squad = squads.Squad(1, [self.player1, self.player2])
        avgPlay = squad.getAveragePlayer()
        expectedHTML = squad.table.__html__()

        expectedHTML = expectedHTML.replace("</tbody>",
                                            ("</tbody>\n<tbody class=avgRow>\n"
                                             "<tr><td><b>Average</b></td>"
                                             "<td>%s</td><td>%s</td>"
                                             "<td>%s</td></tr>\n</tbody>"
                                             % (avgPlay.skate, avgPlay.shoot,
                                                avgPlay.check)))

        with patch("builtins.open", mock_open()) as mock_file:
            html = squad.toHTML()

        self.assertEqual(html, expectedHTML)
