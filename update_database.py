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

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
