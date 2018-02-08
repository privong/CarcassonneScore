#!/usr/bin/env python
"""
Database management for Carcassonne score keeping system.

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

import sys
import argparse
import re
import sqlite3


def parseArgs():
    """
    Command line arguments
    """

    parser = argparse.ArgumentParser(description="Update the Carcassonne \
scoring database.")
    cmds = parser.add_mutually_exclusive_group(required=True)
    cmds.add_argument('-n', '--newplayer', type=str, default=None,
                      nargs='+',
                      help='Add a new player.')
    cmds.add_argument('-e', '--enableexpansion', action='store_true',
                      default=False,
                      help='Enable an expansion.')
    cmds.add_argument('-d', '--disableexpansion', action='store_true',
                      default=False,
                      help='Disable an expansion.')

    return parser.parse_args()


def getExpans(cur, active=True):
    """
    Get a list of (in)active expansions
    """

    command = 'SELECT expansionID,name FROM expansions WHERE active='
    if active:
        command = command + '1'
    else:
        command = command + '0'

    return cur.execute(command).fetchall()


def toggleExpan(cur, ID, activate=True):
    """
    Flip the 
    """
    command = 'UPDATE expansions SET active='
    if activate:
        command = command + '1'
    elif not activate:
        command = command + '0'
    else:
        sys.stderr.write("What have you done?\n")
        sys.exit(-1)

    command = command + ' where expansionID={0:1.0f}'.format(ID)

    cur.execute(command)


def main():
    """
    main routine
    """

    args = parseArgs()

    conn = sqlite3.connect('CarcassonneScore.db')
    cur = conn.cursor()

    VALID = False

    if args.newplayer:
        pname = ' '.join(args.newplayer)
        sys.stdout.write("Adding new player: " + pname)
        sys.stdout.write(" to the database.\n")
        while not VALID:
            ans = input("Is this correct (y/n)? ")
            if re.match('y', ans, re.IGNORECASE):
                cur.execute('INSERT INTO players (name) VALUES ("' + \
                            pname + '")')
                sys.stdout.write(pname + ' added to the database.\n')
                VALID = True
            elif re.match('n', ans, re.IGNORECASE):
                sys.stdout.write('Canceling.\n')
                VALID = True

    if args.enableexpansion:
        expans = getExpans(cur, active=False)
        kwds = ("enable", "inactive")
        activate = True
    elif args.disableexpansion:
        expans = getExpans(cur, active=True)
        kwds = ("disable", "active")
        activate = False

    if args.enableexpansion or args.disableexpansion:
        expnumlist = []
        for expan in expans:
            expnumlist.append(int(expan[0]))
            sys.stdout.write("{0:1.0f}) ".format(expan[0]) + expan[1] + "\n")
        try:
            toggleexp = input("Please enter the " + kwds[1] + ' expansion to ' + kwds[0] + ': ')
            if not list:
                sys.stderr.write("No expansions specified. Exiting.\n")
        except (EOFError, KeyboardInterrupt):
            conn.close()
            sys.exit()
        #TODO actually update the expansions
        try:
            toggleexp = int(toggleexp)
        except:
            sys.stderr.write("Error: invalid input. Please enter a number from the list next time.\n")
            sys.exit()
        if toggleexp not in expnumlist:
            sys.stderr.write("Error: invalid input. Please enter a number from the list next time.\n")
            sys.exit()
        toggleExpan(cur, toggleexp, activate=activate)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
