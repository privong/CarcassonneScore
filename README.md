# Carcassonne Score keeping

Score keeping software for [Carcassonne](https://boardgamegeek.com/boardgame/822/carcassonne) to facilitate statistical analysis of games.

## Requirements

* python 3 (tested under python 3.6.x)
* numpy

## Usage

Before your first game you will need to initalize the sqlite database:

```
$ python create_database.py
```

### Score keeping

Assuming the database has been initialized, you can run a game with:

```
$ python CarcassonneScore.py
```

This launches the interactive shell. Press `?` for a list of commands.

### Analysis

A sample analysis jupyter notebook and a sample sqlite database containing one game is available in the `analysis/` directory.
