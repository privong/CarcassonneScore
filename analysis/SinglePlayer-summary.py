#!/usr/bin/env python
"""
Make a single player summary graphic.
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np


def getArgs():
    """
    Get command line arguments.
    """

    parser = argparse.ArgumentParser(description="Make a single-player summary \
graphic.")
    parser.add_argument('playerID', type=int, action='store', default=None,
                        help='playerID number to analyze.')

    return parser.parse_args()


def main():
    """
    main routine
    """

    args = getArgs()

    # now do other stuff


if __name__ == "__main__":
    main()
