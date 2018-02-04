#!/usr/bin/env python
"""
Make a single game summary graphic.
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np


def getArgs():
    """
    Get command line arguments.
    """

    parser = argparse.ArgumentParser(description="Make a single-game summary \
graphic.")
    parser.add_argument('gameID', type=int, action='store', default=None,
                        help='gameID number to analyze.')

    return parser.parse_args()


def main():
    """
    main routine
    """

    args = getArgs()

    # now do other stuff


if __name__ == "__main__":
    main()
