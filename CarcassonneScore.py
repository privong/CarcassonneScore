#!/usr/bin/env python
"""
Carcassonne score keeping system.
"""

import argparse
import cgame

def getargs():
    """
    Get command line arguments.
    """

    parser = argparse.ArgumentParser(description="Carcassonne score keeping \
system.")
    
    return parser.parse_args()


def main():
    """
    Main routine
    """

    args = getargs()

    mygame = cgame.cgame()

    mygame.runGame()

    sys.stdout.write("Thanks for playing!\n\n")


if __name__ == "__main__":
    main()
