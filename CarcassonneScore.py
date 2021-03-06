#!/usr/bin/env python
"""
Carcassonne score keeping system.

Copyright 2018-2019 George C. Privon

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

import argparse
import sys
import cgame

__version__ = "0.4.4"

def getargs():
    """
    Get command line arguments.
    """

    parser = argparse.ArgumentParser(description="Carcassonne score keeping \
system.")
    parser.add_argument('-c', '--config', default='CarcassonneScore.conf',
                        help='Location of the configuration file.')
    parser.add_argument('--random-exp', default=False,
                         help="Select a random set of active expansions and \
mini-expansions.")

    return parser.parse_args()


def main():
    """
    Main routine
    """

    args = getargs()

    mygame = cgame.cgame(args=args)

    mygame.runGame()

    sys.stdout.write("Thanks for playing!\n\n")


if __name__ == "__main__":
    main()
