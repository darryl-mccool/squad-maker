import squads

from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

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


class TestGetBalancedSquads(TestCase):

    @patch('players.PlayerList.toHTML', MagicMock)
    @patch('squads.Squad.toHTML', MagicMock)
    def testGetBalancedSquads(self):
        numSquads = 2
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        expectedSquads = [squads.Squad(1, [player1, player3]),
                          squads.Squad(2, [player2, player4])]

        balSquads = squads.getBalancedSquads(numSquads, playerList)

        for squad in balSquads:
            print(squad.squadNum)
            for player in squad.players:
                print(player.name)

        for squad in expectedSquads:
            print(squad.squadNum)
            for player in squad.players:
                print(player.name)
        self.assertEqual(balSquads, expectedSquads)

    @patch('players.PlayerList.toHTML', MagicMock)
    @patch('squads.Squad.toHTML', MagicMock)
    def testGetBalancedSquads__OneSquad(self):
        numSquads = 1
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        expectedSquads = [squads.Squad(1, playerList.players)]

        balSquads = squads.getBalancedSquads(numSquads, playerList)
        self.assertEqual(balSquads, expectedSquads)
        self.assertEqual(playerList.players, [])

    @patch('players.PlayerList.toHTML', MagicMock)
    @patch('squads.Squad.toHTML', MagicMock)
    def testGetBalancedSquads__NSquads(self):
        numSquads = 4
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        expectedSquads = [squads.Squad(1, [player4]),
                          squads.Squad(2, [player3]),
                          squads.Squad(3, [player2]),
                          squads.Squad(4, [player1])]

        balSquads = squads.getBalancedSquads(numSquads, playerList)

        self.assertEqual(balSquads, expectedSquads)
        self.assertEqual(playerList.players, [])

    def testGetBalancedSquadsRaisesValueError__GreaterThanNSquads(self):
        numSquads = 5
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        with self.assertRaises(ValueError):
            balSquads = squads.getBalancedSquads(numSquads, playerList)

    def testGetBalancedSquadsRaisesValueError__ZeroSquads(self):
        numSquads = 0
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        with self.assertRaises(ValueError):
            balSquads = squads.getBalancedSquads(numSquads, playerList)

    def testGetBalancedSquadsRaisesValueError__NegSquads(self):
        numSquads = -1
        player1 = Player("99", "Wayne Gretzky", 99, 99, 99)
        player2 = Player("97", "Connor McDavid", 97, 97, 97)
        player3 = Player("123", "Ben Schreiber", 51, 51, 51)
        player4 = Player("404", "Nota RealPlayer", 20, 20, 20)
        playerList = PlayerList([player1, player2, player3, player4])

        with self.assertRaises(ValueError):
            balSquads = squads.getBalancedSquads(numSquads, playerList)
