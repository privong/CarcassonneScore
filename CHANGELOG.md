# Changelog

## 0.4 Series

### 0.4.x (in progress)

#### Enhancements

* Note when a score has not been recorded.

### 0.4.3 (22 May 2019)

#### Enhancements

* Print token type in scoring confirmation message. Update formatting.
* Add "Hills and & Sheep" Expansion.
  To update your database, run this SQLITE statement:
  `update expansions set active=1, tokens="Shepherd", scoretypes="Flock", Ntiles=18, tiletypes="Hill,Vineyard" where expansionID=9;`
* At the end of play and the end of final scoring, print score sorted from highest to lowest score.

#### Bug Fixes

* Update single-game and score distribution demo scripts to generalize color cycler and hatching for larger numbers of players.

### 0.4.2 (21 November 2018)

#### Enhancements

* Add turn length vs turn number plot to `analysis/SampleAnalysis-SingleGame.ipynb`.
* Reorder game initilization so that most of the info can be entered before the player order is determined.
* Announce gameID and location at the start.
* Status printout now shows time elapsed since end of previous turn.
* In the status message, showing the number of tiles played/remaining and the time elapsed since the end of the previous turn is now controlled via options in the configuration file.
* Add `requirements.txt` file.
* Print the player's name when confirming a score entry.

#### Bug fixes

* Fixed tile counting bug when an Abbey is played.
* Fixed missing Abbey score type when Expansion 5 is used.
  This requres running the following command in sqlite3: `update expansions set scoretypes="Abbey" where expansionID=5;`
* Include played Abbey tiles in the total number of tiles played.
* Ensure negative scores cannot be entered.
* Print all players who are scoring when confirming.

### 0.4.1 (18 November 2018)

#### Enhancements

* Add `analysis/README.md` file to briefly explain what the analysis scripts do.
* Add some additional explanatory text to the main `README.md` file.
* Add Expansion 3 (The Princes and the Dragon) to SQL database creation.
* Reorder score recording questions to better match how players seem to naturally report scores.
* Add a command to note that a player played an Abbey tile (if "Abbey & Mayor" expansion is in play). This increments the turn as normal but does not increment the number of tiles played (so that the tiles remaining count remains accurate).

#### Bug fixes

* Fixed bug where `ScoreProbByType.ipynb` sample script failed when showing PDFs for trade token score distributions.
* Use `ORDER BY` in some analysis queries to ensure turn/score information is returned in the proper order.
* Minor plotting code updates in analysis to fix depredations in matplotlib.
* Fix off-by-one error in number of tiles remaining which occurs when The River expansion is in use.

### 0.4.0 (11 November 2018)

#### Enhancements

* add a configuration file specifying the database location
* add a utilities directory for scripts which should not be needed for normal operation but may be useful for working around issues.
* add scoring capability for Trade tokens (Traders & Builders Expansion). Token allocation is not automatically tracked (this can be tracked manually using the scoring comments). Trade token scores are entered during the post-game scoring period.

## 0.3 Series

### 0.3.4 (28 February 2018)

#### Enhancements

* analysis script to look at a player's scoring trends with time

### 0.3.3 (21 February 2018)

#### Enhancements

* Example analysis to show probability distributions of score by score type.

#### Bug fixes

* properly count the starting tile
* fix labeling issue in analysis script
* check validity of player IDs when a score is entered

### 0.3.2 (07 February 2018)

#### Bug fixes

* syntax error in `manage_database.py`

### 0.3.1 (07 February 2018)

#### Bug fixes

* Correct version number in source code

### 0.3.0 (07 February 2018)

#### Enhancements

* new `manage_database.py` script to create and maintain the database
* add database versioning

## 0.2 Series

### 0.2.0 (04 February 2018)

#### Bug fixes

* check inputs

#### Enhancements

* Require a minimum of 2 players
* Implement a check on scores in case bad values are entered
* Sample game data and an analysis notebook in the `analysis/` directory

## 0.1 Series

### 0.1.1 (03 February 2018)

#### Bug fixes

* Add missing score type

### 0.1.0 (03 February 2018)

Initial release.

