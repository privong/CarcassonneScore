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
import sqlite3 as _sqlite3
import numpy as _np


class cgame:
    """
    Carcassonne game object
    """

    def __init__(self):
        """
        Initialize some variables and set up a game
        """

        self.commands = [('r', 'record score and advance turn'),
                         ('t', 'advance turn, no score'),
                         ('b', 'additional turn for a player due to a builder'),
                         ('e', 'end game (or play if already in postgame scoring'),
                         ('s', '(current) score and game status'),
                         ('?', 'print help')]

        self.conn = _sqlite3.connect('CarcassonneScore.db')
        self.cur = self.conn.cursor()

        self.setupGame()


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

        # game state information
        self.state = 0  # 0 for main game, 1 for postgame, 2 for ended game
        self.ntile = 0  # number of tiles played
        self.nbuilder = 0   # number of tiles placed due to builders
        self.totaltiles = 72    # may be increased by expansions

        # get players for this game
        _sys.stdout.write("Collecting player information...\n")
        while self.getPlayers():
            continue

        # get expansions used for this game
        _sys.stdout.write("Collecting expansion information...\n")
        while self.getExpansions():
            continue

        # get general game info (do this after expansions because
        # expansion info is entered into the game table)
        while self.gameInfo():
            continue


    def gameInfo(self):
        """
        Load basic game info
        """

        location = input("Where is the game being played? ")

        starttime = _datetime.utcnow().strftime("%Y-%m-%dT%H:%M")

        self.cur.execute('INSERT INTO games (location, starttime, expansions) VALUES ("' + location + '","' + starttime + '","' + ','.join(["{0:d}".format(x) for x in self.expansionIDs]) + '")')

        gID = self.cur.execute('select last_insert_rowid();').fetchall()[0]

        self.gameID = gID[0]


    def getPlayers(self):
        """
        Get a list of possible players from the database
        """

        self.players = []

        dbplayers = self.cur.execute('''SELECT * FROM players''').fetchall()

        if len(dbplayers):
            for dbplayer in dbplayers:
                _sys.stdout.write("{0:d}) ".format(dbplayer[0]) + dbplayer[1] + '\n')
            playerinput = input("Please list the IDs for the players in this game (in order of play): ")
            playerIDs = [int(x) for x in playerinput.split()]

            for playerID in playerIDs:
                matched = False
                for dbplayer in dbplayers:
                    if playerID == dbplayer[0]:
                        self.players.append((playerID, dbplayer[1]))
                        matched = True
                        continue
                if not matched:
                    _sys.stderr.write("Error: player ID {0:d} does not match an option from the list.\n".format(playerID))
                    return 1
        else:
            _sys.stderr.write("Error: players table empty. Exiting.\n")
            _sys.exit(-1)

        return 0


    def getExpansions(self):
        """
        Get a list of playable expansions
        """

        self.expansionIDs = []

        for minisel in range(0, 2):
            if minisel:
                exptype = "mini"
            else:
                exptype = "large"
            dbexpans = self.cur.execute('''SELECT expansionID,name,Ntiles FROM expansions WHERE active==1 and mini=={0:d}'''.format(minisel)).fetchall()

            if len(dbexpans):
                for dbexpan in dbexpans:
                    _sys.stdout.write("{0:d}) ".format(dbexpan[0]) + dbexpan[1] + '\n')
                expaninput = input("Please list the numbers for the " + exptype + " used in this game: ")
                expanIDs = [int(x) for x in expaninput.split()]
                for expanID in expanIDs:
                    matched = False
                    for dbexpan in dbexpans:
                        if expanID == dbexpan[0]:
                            self.expansionIDs.append(expanID)
                            self.totaltiles += dbexpan[2]
                            matched = True
                            continue
                    if not matched:
                        _sys.stderr.write("Error: expansion ID {0:d} does not match an option from the list.\n".format(expanID))
                        return 1
            else:
                _sys.stdout.write("No active " + exptype + " expansions found. Continuing.\n")
        return 0


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

        advanceTurn(builder=BUILDERUSED)

        return 0


    def advanceTurn(self, builder=False):
        """
        Make a new entry in the turns table
        """

        cmdtime = _datetime.utcnow().strftime("%Y-%m-%dT%H:%M")

        command = '''INSERT INTO turns VALUES ({0:d}, {1:d}, "'''.format(self.gameID, self.ntile)
        command = command + cmdtime + '"'
        if builder:
            bID = 1
        else:
            bID = 0

        # compute playerID based on the turn number minus nbuilders / number of players
        playerID = self.playerIDs[(self.ntile- self.nbuilder) / len(playerIDs)]
        command = command + ', {0:d}, {1:d})'.format(bID, playerID)

        self.cur.execute(command)

        self.ntile += 1
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
                prompt = "round: {0:d}, turn: {1:d} > ".format(int(_np.floor((self.ntile-self.nbuilder) / len(self.players))),
                                                               self.ntile-self.nbuilder)

            try:
                cmd = input(prompt)
            except (EOFError, KeyboardInterrupt):
                _sys.stderr.write('Improper input. Please retry\n')
                self.showCommands()

            if _re.match('e', cmd, _re.IGNORECASE):
                self.advanceState()
            elif _re.match('s', cmd, _re.IGNORECASE):
                self.printStatus(tilestats=True)
            elif _re.match('n', cmd, _re.IGNORECASE):
                self.advanceTurn()
            elif _re.match('r', cmd, _re.IGNORECASE):
                self.recordScore()
            elif _re.match('t', cmd, _re.IGNORECASE):
                self.advanceTurn(builder=False)
            elif _re.match('b', cmd, _re.IGNORECASE):
                self.advanceTurn(builder=True)
            elif _re.match('\?', cmd, _re.IGNORECASE):
                self.showCommands()
            else:
                _sys.stderr.write('Command not understood. Please try again.\n')
                self.showCommands()

        if state == 2:
            #game is over. write end time to the games table
            time = _datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
            self.cur.execute('''UPDATE games SET endtime = "''' + time + '''" WHERE gameID = ''' + str(gameID))
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

        _sys.stdout.write('\nCurrent Score\n')

        for player in self.players:
            a = self.cur.execute('SELECT points FROM scores WHERE gameID={0:d} and playerID={1:d}'.format(self.gameID, player[0]))
            res = a.fetchall()
            score = _np.sum(res)

            _sys.stdout.write('\t' + player[1]+ ': {0:1.0f}'.format(score) + '\n')

        _sys.stdout.write("{0:1.0f} tiles played, {1:1.0f} remaining.\n\n".format(self.ntile,
                                                                                  self.totaltiles - self.ntile))
