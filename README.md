# Carcassonne Score keeping

Score keeping software for [Carcassonne](https://boardgamegeek.com/boardgame/822/carcassonne) to facilitate statistical analysis of games.

## Requirements

* python 3 (tested under python 3.6.x)
* numpy
* matplotlib (for analysis scripts)

## Usage

Before your first game you will need to initialize the sqlite database:

```
$ python manage_database.py --init
```

### Score keeping

Assuming the database has been initialized, you can run a game with:

```
$ python CarcassonneScore.py
```

This launches the interactive shell. Press `?` for a list of commands.

### Database Maintenance

To update the database (add new players toggle availability of expansions), use the `manage_database.py` command. For example, to add a new player:

```
$ python manage_database.py -n NEW PLAYER
```

Use `python manage_database.py -h` to see the full list of options.


### Analysis

Some jupyter notebooks with sample analysis and a sample sqlite database containing one game are available in the `analysis/` directory.

### Miscellaneous Utilities

The `utilities/` directory contains scripts which may be useful for correcting issues, but these should not be needed for normal operations.
