# Win probability in cricket

An attempt to calculate the win probability for every ball in a one-day international (ODI) cricket match.

This project began after I watched India play Zimbabwe in the 2015 Cricket World Cup. [India won with 8 balls to spare](http://www.espncricinfo.com/icc-cricket-world-cup-2015/engine/match/656475.html?view=runrate), despite my belief while watching that Zimbabwe had the game in hand.

Sources:
* https://saidee27.wordpress.com/2014/09/29/in-game-win-probability-twenty20-cricket/
* http://thespread.us/

## To get started:

```
$ python get_scripts/01_download.py
$ python get_scripts/02_makemaster.py
$ python get_scripts/03_calcs.py
```

This will do the following (and take a few minutes to complete):

1. Grab the latest .zip of ODI data from [Cricsheet.org](http://cricsheet.org/) and unpack it to a folder named `all_odis`.
2. Create two files in `master_data` folder:
  * `odi_info.csv` (about 0.1 MB) -- information about the game such as location, teams, toss, etc.
  * `odi_ballbyball.csv` (about 50 MB) -- every ball in every ODI match
3. Process the master files into `odi_ballinfotrim.csv` that merges some ball and match info and has extra columns with basic calculation about the game state.