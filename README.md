# Carcassonne Score keeping

Score keeping software for [Carcassonne](https://boardgamegeek.com/boardgame/822/carcassonne) to facilitate statistical analysis of games.
Information (players, games, scores, expansions) are stored in a sqlite3 database.
The location of this database defaults to `CarcassonneScore.db`, but can be specified in the `CarcassonneScore.conf` configuration file.

## Requirements

* python 3 (currently tested on python 3.7.x, but has previously worked with python 3.6.x)
* numpy
* matplotlib (only needed for for analysis scripts)

## Usage

Before your first game you will need to initialize the sqlite database:

```
$ python manage_database.py --init
```

### Score keeping

After a database has been initialized, you can score a game with:

```
$ python CarcassonneScore.py
```

This launches the interactive shell which sets up a game (gets the names and order of players, list of active expansions, and other information).
Within this shell various commands are available to record scores, advance to a next player's turn, and end the game.
Press `?` within the shell for a list of commands (note that the list of available commands may change depending on the expansions being played and whether the game is in active tile-placing mode or post-game scoring mode).

### Database Maintenance

To update the database (e.g., to add new players or toggle availability of expansions), use the `manage_database.py` command. For example, to add a new player:

```
$ python manage_database.py -n NEW PLAYER
```

Use `python manage_database.py -h` to see the full list of options.

### Analysis

Some jupyter notebooks with sample analysis and a sample sqlite database containing one game are available in the `analysis/` directory.

### Miscellaneous Utilities

The `utilities/` directory contains scripts which may be useful for correcting issues, but these should not be needed for normal operations.
