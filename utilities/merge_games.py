#!/usr/bin/env python
"""
In the event the scoring program is killed or crashes mid-game there is 
currently no way to resume a game, so a new game must be started.
This script takes a list of games (provided in the `gameIDs` list) and
combines them into the first game in the list.

It should work fine, but I'd recommend backing up your CarcassonneScore sqlite
database, just in case.
"""

import sqlite3


# edit this to say which gameIDs will need to combined into a single game
# You'll need to look at the actual sqlite database.
gameIDs = (8, 9, 10)

conn = sqlite3.connect('CarcassonneScore.db')
cur = conn.cursor()

# update turns and scores
lastturn = []
lastscore = []
for game in gameIDs:
    lastturn.append(cur.execute('SELECT turnNum FROM turns WHERE gameID={0:1.0f} ORDER BY turnNum DESC LIMIT 1;'.format(game)).fetchall()[0][0])
    lastscore.append(cur.execute('SELECT scoreID FROM scores WHERE gameID={0:1.0f} ORDER BY scoreID DESC LIMIT 1;'.format(game)).fetchall()[0][0])

curturn = lastturn[0]
curscore = lastscore[0]

for i, game in enumerate(gameIDs[1:]):
    print("Fixing game {0:1.0f}".format(game))
    # get a list of all the turns
    turns = cur.execute('SELECT gameID,turnNum FROM turns WHERE gameID={0:1.0f}'.format(game)).fetchall()
    for turn in turns:
        curturn += 1
        # update turns database
        command = 'UPDATE turns SET (gameID,turnNum) = ({0:1.0f},{1:1.0f}) WHERE gameID={2:1.0f} AND turnNum={3:1.0f};'.format(gameIDs[0],curturn,game,turn[1])
        print(command)
        cur.execute(command)
        # update all scores
        command = 'SELECT gameID,turnNum,scoreID from scores where gameID={0:1.0f} and turnNum={1:1.0f}'.format(game,
                                                                                                                turn[1])

        turnscores = cur.execute(command).fetchall()
        for score in turnscores:
            curscore += 1
            command = 'UPDATE scores SET (gameID,turnNum,scoreID) = ({0:1.0f},{1:1.0f},{2:1.0f}) WHERE gameID={3:1.0f} AND turnNum={4:1.0f};'.format(gameIDs[0], curturn, curscore, game, turn[1])
            cur.execute(command)

# fix the end of game scores
curturn += 1
command = 'SELECT gameID,turnNum,scoreID from scores where gameID={0:1.0f} and turnNum={1:1.0f}'.format(game,
                                                                                                        14)

turnscores = cur.execute(command).fetchall()
for score in turnscores:
    curscore += 1
    command = 'UPDATE scores SET (gameID,turnNum,scoreID) = ({0:1.0f},{1:1.0f},{2:1.0f}) WHERE gameID={3:1.0f} AND turnNum={4:1.0f};'.format(gameIDs[0], curturn, curscore, game, 14)
    cur.execute(command)

conn.commit()
conn.close()
