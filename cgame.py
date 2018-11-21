#!/usr/bin/env python
"""
Class definition for Carcassonne score keeping system.

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

import os as _os
import re as _re
import sys as _sys
import configparser as _configparser
from datetime import datetime as _datetime
import sqlite3 as _sqlite3
import numpy as _np


class cgame:
    """
    Carcassonne game object
    """

    def __init__(self, config='CarcassonneScore.db'):
        """
        Initialize some variables and set up a game
        """

        self.commands = [('r', 'record score'),
                         ('n', 'next turn'),
                         ('e', 'end game (or end play if already in postgame scoring)'),
                         ('s', '(current) score and game status'),
                         ('q', 'quit (will be removed for real gameplay'),
                         ('?', 'print help')]

        self.loadConfig(config)

        self.conn = _sqlite3.connect(self.config.get('CarcassonneScore', 'DBNAME'))
        self.cur = self.conn.cursor()

        self.timefmt = "%Y-%m-%dT%H:%M:%S"
        self.setupGame()


    def loadConfig(self, cfile):
        """
        Load configuration file
        """

        if not _os.path.isfile(cfile):
            _sys.stderr.write("Error: could not find configuration file '" + cfile + "'\n")
            _sys.exit()

        self.config = _configparser.RawConfigParser()
        self.config.read(cfile)

        # set up a preferences dictionary
        self.preferences = {}
        self.preferences['SHOWTILES'] = self.config['Status'].getboolean('SHOWTILES')
        self.preferences['SHOWTIME'] = self.config['Status'].getboolean('SHOWTIME')


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
        self.nscore = 0
        self.ntile = 1  # number of tiles played
        self.nbuilder = 0   # number of tiles placed due to builders
        self.nabbey = 0     # number of Abbey tiles played
        self.totaltiles = 72    # may be increased by expansions

        self.tokens = ["Meeple"]
        self.tiletypes = []
        self.scoretypes = ["Meadow", "City", "Road", "Monastery"]

        # get general game info (do this after expansions because
        # expansion info is entered into the game table)
        while self.gameInfo():
            continue


    def gameInfo(self):
        """
        Load basic game info
        """

        location = input("Where is the game being played? ")

        # get expansions used for this game
        _sys.stdout.write("Collecting expansion information...\n")
        while self.getExpansions():
            continue

        # get players for this game
        _sys.stdout.write("Collecting player information...\n")
        while self.getPlayers():
            continue

        self.starttime = _datetime.utcnow()
        self.lastturn = self.starttime
        starttime = self.starttime.strftime(self.timefmt)

        self.cur.execute('INSERT INTO games (location, starttime, expansions) VALUES ("' + location + '","' + starttime + '","' + ','.join(["{0:d}".format(x) for x in self.expansionIDs]) + '")')

        gID = self.cur.execute('select last_insert_rowid();').fetchall()[0]

        self.conn.commit()

        self.gameID = gID[0]
        
        _sys.stdout.write("Starting game #{0:d}".format(self.gameID))
        if location:
            _sys.stdout.write(" in " + location)
        _sys.stdout.write(".\n")


    def getPlayers(self):
        """
        Get a list of possible players from the database
        """

        self.players = []

        dbplayers = self.cur.execute('''SELECT * FROM players''').fetchall()

        if len(dbplayers):
            for dbplayer in dbplayers:
                _sys.stdout.write("{0:d}) ".format(dbplayer[0]) + dbplayer[1] + '\n')
            VALID = False
            while not VALID:
                playerinput = input("Please list the IDs for the players in this game (in order of play): ")
                try:
                    playerIDs = [int(x) for x in playerinput.split()]
                    VALID = True
                except:
                    _sys.stderr.write("Error: input must be a list of integers separated by spaces.\n")

            if len(playerIDs) < 2:
                _sys.stderr.write("Playing alone? You need at least one opponent!\n")
                return 1

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
        Get a list of playable expansions.
        Ask the user which ones are active.
        Based on the list, add token, tile, and score types to the basic list.
        """

        self.expansionIDs = []

        for minisel in range(0, 2):
            if minisel:
                exptype = "mini"
            else:
                exptype = "large"
            dbexpans = self.cur.execute('''SELECT expansionID,name,tokens,Ntiles,tiletypes,scoretypes FROM expansions WHERE active==1 and mini=={0:d}'''.format(minisel)).fetchall()

            if len(dbexpans):
                for dbexpan in dbexpans:
                    _sys.stdout.write("{0:d}) ".format(dbexpan[0]) + dbexpan[1] + '\n')
                VALID = False
                while not VALID:
                    expaninput = input("Please list the numbers for the " + exptype + " used in this game: ")
                    try:
                        expanIDs = [int(x) for x in expaninput.split()]
                        VALID = True
                    except:
                        _sys.stderr.write("Error: input must be a list of integers separated by spaces.\n")
                for expanID in expanIDs:
                    matched = False
                    if expanID == 2:
                        # add the builder cmd if Traders & Builders is used
                        self.commands.append(('b', 'additional turn for a player due to a builder (use for the 2nd play by a player)'))
                    elif expanID == 5:
                        # add Abbey placement command
                        self.commands.append(('a', 'Player places an abbey tile instead of a tile drawn from the pile'))
                    elif expanID == 101:
                        # decrement totaltiles because the base pack starting tile is not used
                        self.totaltiles -= 1
                    for dbexpan in dbexpans:
                        if expanID == dbexpan[0]:
                            self.expansionIDs.append(expanID)
                            self.totaltiles += dbexpan[3]
                            ttypes = dbexpan[2].split(',')
                            if len(ttypes):
                                # add new types of tokens
                                for token in ttypes:
                                    if token:
                                        self.tokens.append(token)
                            tiletypes = dbexpan[4].split(',')
                            if len(tiletypes):
                                # add special tiles
                                for tile in tiletypes:
                                    if tile:
                                        self.tiletypes.append(tile)
                            stypes = dbexpan[5].split(',')
                            if len(stypes):
                                # add new types of scoring
                                for stype in stypes:
                                    if stype:
                                        self.scoretypes.append(stype)
                            matched = True
                            continue
                    if not matched:
                        _sys.stderr.write("Error: expansion ID {0:d} does not match an option from the list.\n".format(expanID))
                        return 1
            else:
                _sys.stdout.write("No active " + exptype + " expansions found. Continuing.\n")
        return 0


    def recordScore(self):
        """
        Record a score event in the game
        """

        score = {'playerIDs': -1,
                 'ingame' : 1,
                 'points' : 0,
                 'scoretype': '',
                 'sharedscore': 0,
                 'tokens': '',
                 'extras': '',
                 'comments': ''}

        if self.state:
            score['ingame'] = 0

        # ask the user which player scored
        VALID = False
        while not VALID:
            for player in self.players:
                _sys.stdout.write("{0:d}) ".format(player[0]) + player[1] + "\n")
            scoreplayers = input("Please enter the numbers for the players who scored: ")
            try:
                score['playerIDs'] = [int(x) for x in scoreplayers.split()]
                if not len(score['playerIDs']):
                    _sys.stderr.write("There must be at least one player.\n")
                    continue
                elif self.checkPlayers(score['playerIDs']):
                    _sys.stderr.write("At least one player entered is not playing this game.\n")
                else:
                    VALID = True
            except:
                _sys.stderr.write("Error, could not parse players list.\n")
                continue
            if len(score['playerIDs']) > 1:
                score['sharedscore'] = 1

        # see which token scored
        # really this should be expanded to allow multiple token types for one score
        if score['scoretype'] == 'Trade token':
            score['tokens'] = 'none'
        elif len(self.tokens) > 1:
            VALID = False
            while not VALID:
                for i, token in enumerate(self.tokens):
                    _sys.stdout.write("{0:d}) ".format(i+1) + token + "\n")
                tID = input("Please select the token type(s): ")
                try:
                    score['tokens'] = ','.join(self.tokens[int(x)-1] for x in tID.split())
                    VALID = True
                except:
                    _sys.stderr.write("'" + tID + "' is not a valid token.\n")
                    continue
        else:
            score['tokens'] = self.tokens[0]

        # get the score type
        VALID = False
        while not VALID:
            for i, stype in enumerate(self.scoretypes):
                _sys.stdout.write("{0:d}) ".format(i+1) + stype + "\n")
            # here i want a list of valid score types
            stype = input("Please select the score type: ")
            try:
                score['scoretype'] = self.scoretypes[int(stype)-1]
                VALID = True
            except:
                _sys.stderr.write("'" + stype + "' is not a valid score type.\n")
                continue

        # get points for score
        VALID = False
        while not VALID:
            points = input("Enter the total number of points: ")
            try:
                score['points'] = int(points)
                VALID = True
            except:
                _sys.stderr.write("'" + points + "' is not a valid score.\n")
                continue

        score['comments'] = input("Enter any comments you would like saved (a single line): ")

        # check score input to make sure it's correct
        _sys.stdout.write('Player {0:d} scores {1:d} points on a '.format(score['playerIDs'][0], score['points']) + score['scoretype'] + '.\n')
        answer = input("Is this correct? (y/n) ")
        if not _re.match('y', answer, _re.IGNORECASE):
            return 1

        # now construct a SQL query
        for player in score['playerIDs']:
            command = 'INSERT INTO scores VALUES ({0:d},'.format(self.gameID)
            command = command + '{0:d},'.format(player)
            command = command + '{0:d},{1:d},'.format(self.ntile,
                                                       self.nscore)
            command = command + '{0:d},{1:d},'.format(score['ingame'],
                                                       score['points'])
            command = command + '"' + score['scoretype'] + '",'
            command = command + '{0:d},'.format(score['sharedscore'])
            command = command + '"' + score['tokens'] + '",'
            command = command + '"' + score['extras'] + '",'
            command = command + '"' + score['comments'] + '")'
            self.cur.execute(command)


        self.conn.commit()
        # now increment the score number
        self.nscore += 1

        # newline after score for aesthetics
        _sys.stdout.write("\n")

        return 0


    def advanceTurn(self, builder=False, abbey=False):
        """
        Make a new entry in the turns table
        - builder: if True, give the user another turn
        - abbey: if True, the turn is advanced as normal, but don't increment the number of tiles
        """

        self.lastturn = _datetime.utcnow()
        cmdtime = self.lastturn.strftime(self.timefmt)

        command = '''INSERT INTO turns VALUES ({0:d}, {1:d}, "'''.format(self.gameID, self.ntile)
        command = command + cmdtime + '"'
        if builder:
            bID = 1
        elif abbey:
            bID = 2
        else:
            bID = 0

        # compute playerID based on the turn number minus nbuilders / number of players
        player = self.getCurrentPlayer()
        command = command + ', {0:d}, {1:d})'.format(bID, player[0])

        self.cur.execute(command)
        self.conn.commit()

        # only increment the number of tiles played if the player did not play an Abbey
        if not abbey:
            self.ntile += 1
        else:
            self.nabbey += 1

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
                player = self.getCurrentPlayer()
                prompt = "round: {0:d}, turn: {1:d} ".format(int(_np.floor((self.ntile-self.nbuilder-1) / len(self.players))),
                                                               self.ntile-self.nbuilder)
                prompt = prompt + "(" + player[1] + ") > "

            try:
                cmd = input(prompt)
            except (EOFError, KeyboardInterrupt):
                _sys.stderr.write('Improper input. Please retry\n')
                self.showCommands()

            if _re.match('e', cmd, _re.IGNORECASE):
                self.advanceState()
            elif _re.match('q', cmd, _re.IGNORECASE):
                _sys.exit(0)
            elif _re.match('s', cmd, _re.IGNORECASE):
                if self.state:
                    self.printStatus(tilestats=False)
                else:
                    self.printStatus(tilestats=self.preferences['SHOWTILES'],
                                     timestats=self.preferences['SHOWTIME'])
            elif _re.match('n', cmd, _re.IGNORECASE):
                self.advanceTurn(builder=False,
                                 abbey=False)
            elif _re.match('r', cmd, _re.IGNORECASE):
                self.recordScore()
            elif _re.match('b', cmd, _re.IGNORECASE):
                self.advanceTurn(builder=True,
                                 abbey=False)
            elif _re.match('a', cmd, _re.IGNORECASE):
                self.advanceTurn(builder=False,
                                 abbey=True)
            elif _re.match('\?', cmd, _re.IGNORECASE):
                self.showCommands()
            else:
                _sys.stderr.write('Command not understood. Please try again.\n')
                self.showCommands()

        if self.state == 2:
            #game is over. write end time to the games table
            time = _datetime.utcnow().strftime(self.timefmt)
            self.cur.execute('''UPDATE games SET endtime = "''' + time + '''" WHERE gameID = ''' + str(self.gameID))
            self.conn.commit()

        _sys.stdout.write("Game over!\n")

        self.printStatus(tilestats=False, sort=True)

        self.conn.close()

        #### Is there a way to capture "ineffective" uses? For example,
        #### meeples that don't score points because they end up in a meadow that's
        #### controled by someone else?

        return 0


    def advanceState(self):
        """
        End the main part of play or finish the game.
        Does not change the turn number, so turn should be ended before ending
        the game.
        """

        self.state += 1

        if self.state < 2:
            self.commands = [('r', 'record score'),
                             ('e', 'end game (or end play if already in postgame scoring)'),
                             ('s', '(current) score and game status')]
            # add trade token scoring to the game scoring options
            if 2 in self.expansionIDs:
                self.scoretypes.append('Trade token')
            self.commands.append(('?', 'print help'))

            _sys.stdout.write("At the end of regulation... ")
            self.printStatus(tilestats=False, sort=True)


    def printStatus(self, tilestats=False, timestats=False, sort=False):
        """
        Print the total score (current or final) for the specified gameID
        tilestats controls printing info on the number of tiles played/remaining
        sort will trigger sorting by score
        timestats will print out some information about time elapsed (game and turn)
        """

        _sys.stdout.write('\n')
        if not self.state:
            _sys.stdout.write('Current ')
        _sys.stdout.write('Score\n')

        for player in self.players:
            a = self.cur.execute('SELECT points FROM scores WHERE gameID={0:d} and playerID={1:d}'.format(self.gameID, player[0]))
            res = a.fetchall()
            score = _np.sum(res)

            _sys.stdout.write('\t' + player[1]+ ': {0:1.0f}'.format(score) + '\n')

        _sys.stdout.write('\n')

        if tilestats:
            _sys.stdout.write("{0:1.0f} tiles played, {1:1.0f} remaining.\n\n".format(self.ntile + self.nabbey,
                                                                                      self.totaltiles - self.ntile))

        if timestats:
            gamedt = _datetime.utcnow() - self.starttime
            turndt = _datetime.utcnow() - self.lastturn

            #_sys.stdout.write('Game time elapsed: ' + gamedt + '\n')
            _sys.stdout.write('Time since last turn: {0:1.0f} seconds'.format(turndt.total_seconds()) + '\n\n')



    def getCurrentPlayer(self):
        """
        Return the current player, determined by the turn number
        """

        return self.players[int((self.ntile + self.nabbey - self.nbuilder - 1) % len(self.players))]


    def checkPlayers(self, trial):
        """
        Check to make sure all members of `trial` are in `comp`. If so, return
        0. Otherwise return a list containing the missing members.
        """

        playerIDs = [x[0] for x in self.players]

        missing = []
        for obj in trial:
            if obj not in playerIDs:
                missing.append(obj)

        if len(missing):
            return missing
        else:
            return 0
