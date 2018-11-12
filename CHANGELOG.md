# Changelog

## 0.4 Series

### 0.4.1 (in progress)

#### Bug fixes

* Fixed bug where `ScoreProbByType.ipynb` sample script failed when showing PDFs for trade token score distributions.

### 0.4.0 (11 November 2018)

#### Enhancements

* add a configuration file specifying the database location
* add a utilities directory for scripts which should not be needed for normal operation but may be useful for working around issues.
* add scoring capability for Trade tokens (Traders & Builders Expanion). Token allocation is not automatically tracked (this can be tracked manually using the scoring comments). Trade token scores are entered during the post-game scoring period.

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

