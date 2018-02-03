#!/usr/bin/env python
"""
Class defenition for Carcassonne score keeping system.

Copyright 2018 George C. Privon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re as _re
import sys as _sys
from datetime import datetime as _datetime
import numpy as _np


class cgame:
    """
    Carcassonne game object
    """

    def __init__(self):
        """
        Initialize some variables and set up a game
        """

        self.commands = [('n', 'next round'),
                         ('r', 'record score and advance turn'),
                         ('t', 'advance turn, no score'),
                         ('b', 'additional turn for a player due to a builder'),
                         ('e', 'end game (or play if already in postgame scoring'),
                         ('s', '(current) score and game status'),
                         ('?', 'print help')]
        setupGame()


    def showCommands(self):
        """
        Print out a list of valid commands for in-game play.
        """

        _sys.stderr.write('Possible commands:\n')
        for entry in self.commands:
            _sys.stderr.write('\t' + entry[0] + ': ' + entry[1] + '\n')


    def setupGame(self):
        """
        Initialize a game
        """

        # check to see if there's a game which has not yet been finished (i.e., has a starttime but no endtime). If there is, resume it. Otherwise:
        # generate a new game ID and enter a start time
        # get a list of players (from database list)
        # have user input which expansions are being used
        time = _datetime.utcnow().strftime("%Y-%m-%dT%H:%M")

        # insert this into the database

        # general information
        self.gameID =
        # array of tuples with playerID and name from DB
        self.players =
        self.expansionIDs =

        # game state information
        self.state = 0  # 0 for main game, 1 for postgame, 2 for ended game
        self.ntile = 1  # number of tiles played
        self.nbuilder = 0   # number of tiles placed due to builders


    def recordScore(gameID, playerIDs, expansionIDs, cround, state):
        """
        Record a score event in the game
        """

        if state:
            ingame = 0

        pname = getPlayerNames(playerIDs)


       # for i, pname in enumerate(pname):

        pID = input("")

        # if the builder was used
        BUILDERUSED = True

        advanceTurn(cmdtime, gameID, playerID, nturn, builder=BUILDERUSED)

        return 0


    def advanceTurn(self, builder=False):
        """
        Make a new entry in the turns table
        """

        command = '''INSERT INTO turns VALUES ({0:d}, {1:d}, '''.format(self.gameID, self.nturn)
        command = command + cmdtime
        if builder:
            bID = 1
        else:
            bID = 0

        # compute playerID based on the turn number minus nbuilders / number of players
        playerID = playerIDs[(nturns - nbuilder) / lnen(playerIDs)]
        command = command + ', {0:d}, {1:d})'.format(bID, playerID)

        c.execute(command)

        self.nturn += 1
        if builder:
            self.nbuilder += 1


    def runGame(self):
        """
        Main routine for entering games
        """

        # here wait for input for scores, advancing to next round, or completion of game

        # for each step of entry, present a series of options, based on the list
        # of playerIDs and expansions

        while self.state < 2:
            # set up prompt based on current round
            if self.state:
                prompt = "postgame > "
            else:
                prompt = "round: {0:d}, turn: {1:d} > ".format(1 + _np.floor((self.nturn-self.nbuilder) / len(self.playerIDs)),
                                                               self.nturn-self.nbuilder)

            try:
                text = input(prompt)
            except (EOFError, KeyboardInterrupt):
                _sys.stderr.write('Improper input. Please retry\n')
                showCommands()

            if _re.match('e', cmd, _re.IGNORECASE):
                advanceState()
            elif _re.match('s', cmd, _re.IGNORECASE):
                printStatus(tilestats=True)
            elif _re.match('n', cmd, _re.IGNORECASE):
                advanceTurn()
            elif _re.match('r', cmd, _re.IGNORECASE):
                recordScore()
            elif _re.match('t', cmd, _re.IGNORECASE):
                advanceTurn(builder=False)
            elif _re.match('b', cmd, _re.IGNORECASE):
                advanceTurn(builder=True)
            elif _re.match('?'. cmd, _re.IGNORECASE):
                showCommands()
            else:
                _sys.stderr.write('Command not understood. Please try again.\n')
                showCommands()

        if state == 2:
            #game is over. write end time to the games table
            time = _datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
            c.execute('''UPDATE games SET endtime = "''' + time + '''" WHERE gameID = ''' + str(gameID))
            conn.commit()

        printStatus(tilestats=False)

        #### Is there a way to capture "ineffective" uses? For example,
        #### meeples that don't score points because they end up in a meadow that's
        #### controled by someone else?

        return 0


    def printStatus(self, tilestats=False):
        """
        Print the total score (current or final) for the specified gameID
        """

        for playerID in self.playerIDs:
            pname = c.execute('SELECT name FROM players WHERE playerID={0:d}'.format(playerID[0])).fetchall()[0]
            a = c.execute('SELECT points FROM scores WHER gameID={0:d} and playerID={1:d}'.format(self.gameID, playerID[0]))
            res = a.fetchall()
            score = _np.sum(res)

            print(pname + ': {0:d}'.format(score))

        print("{0:d} tiles played out of {1:d} total ({2:d} remaining).".format(self.ntiles,
                                                                                self.totaltiles,
                                                                                self.totaltiles - self.ntiles)
