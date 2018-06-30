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


def getBalancedSquads(numSquads, playerList):
    """
    Dynamically generate closely-balanced squads of players from a given list

    The List of available players is sorted in order of the sum of all of
    their skills. After sorting, each squad in the desired number of squads
    takes the next best player, until it has reached the maximum number of
    players that it can have in order for the given list of players to be
    split into the desired number of squads.

    Errors if the number of desired squads is greater than the number of
    available players, or if number of desired squads is less than one.

    Special Cases:
        1 squad:    When only one squad is needed, all players are moved from
                    the waiting list into the squad.

        numPlayers squads:  When the number of players is equal to the number
                            of desired squads, each player is placed onto their
                            own squad, bypassing the need for calculations

    FUTURE OPTIMIZATION: Once a roughly balanced team is generated, go through
    and attempt to balance further by swapping players between teams
    """
    squads = []
    numPlayers = len(playerList.players)
    if(numSquads > numPlayers):
        raise ValueError(("Number of Squads cannot be greater then number of "
                          "players. %d squads attempted, %d players available."
                          % (numSquads, numPlayers)))
    elif(numSquads < 1):
        raise ValueError(("Number of Squads must be greater than one,"
                          "%d given" % numSquads))
    elif(numSquads == 1):
        newSquad = Squad(1, playerList.players)
        squads.append(newSquad)
        newSquad.toHTML()
        playerList.players = []
    elif(numSquads == numPlayers):
        for i in range(numPlayers):
            newSquad = Squad(i+1, [playerList.players.pop()])
            squads.append(newSquad)
            newSquad.toHTML()
    else:
        squadSize = numPlayers//numSquads

        squadPlayers = [[] for i in range(numSquads)]

        tourney = sorted(playerList.players,
                         key=(lambda x: sum([x.skate, x.shoot, x.check])))

        for j in range(squadSize):
            for squad in squadPlayers:
                pick = tourney.pop()
                squad.append(pick)
                playerList.players.remove(pick)

        for i, squad in enumerate(squadPlayers):
            newSquad = Squad(i+1, squad)
            squads.append(newSquad)
            newSquad.toHTML()

    playerList.toHTML()
    return squads
