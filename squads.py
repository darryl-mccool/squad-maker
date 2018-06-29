from players import Player, PlayerList, PlayerTable


AVERAGENAME = 'Average'


class Squad(PlayerList):
    """Representation of a Squad

    A squad is a group of players, with an identifying number.

    When printing out to HTML, the last entry in the squad contains
    the average values for each of the skills across the team.
    """
    def __init__(self, squadNum, players):
        """
        Create a Squad
        """
        self.squadNum = squadNum
        self.players = players
        self.updateTable()

    def getAveragePlayer(self):
        """
        Get a player that represents the average of each of the
        skills across the whole team
        """
        skateSum = 0
        shootSum = 0
        checkSum = 0
        for player in self.players:
            skateSum += player.skate
            shootSum += player.shoot
            checkSum += player.check

        pLen = len(self.players)
        return Player(None, AVERAGENAME, skateSum//pLen,
                      shootSum//pLen, checkSum//pLen)

    def toHTML(self):
        """
        Output the squad as a table to an HTML file with its corresponding
        squad number, and the average of all skills on the team at the
        bottom.
        """
        avgPlay = self.getAveragePlayer()
        self.updateTable()
        html = self.table.__html__()

        html = html.replace("</tbody>",
                            ("</tbody>\n<tbody class=avgRow>\n<tr>"
                             "<td><b>%s</b></td><td>%s</td><td>%s</td>"
                             "<td>%s</td></tr>\n</tbody>"
                             % (avgPlay.name, avgPlay.skate,
                                avgPlay.shoot, avgPlay.check)))

        return html
