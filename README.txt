Step 1) compileBettingLines.py and txtToCsv.py create CSVs of betting data with game results; advStatsCleanUp.py and adjAdvStatsCleanUp.py create respective forward looking season average CSVs for S&P+ stats
Step 2) eloRating.py uses betting CSVs to create Elo rankings starting in 1999 and includes them in the betting CSVs
Step 3) combineFwdLookingStats.py to merge base S&P+ stats with my adjusted S&P+ stats
Step 4) finalData.py creates "bigboy.csv", a file containing all S&P+ stats and all betting data for each team for each week they play
Step 5) recruitingStats.py adds columns for the rating of the Freshman, Sophomore, etc recruiting classes; coachingStats.py adds column "Coach WPAR", Win Percentage Above Replacement
Step 6) playByPlay.py to make playByPlay CSVs and regStats.py to get that data to bigboy
Step 7) teamGameStats.py to make new CSVs and miscStats.py to get that data to bigboy
Step 8) bigboyConvert.py formats each row to be a single matchup (for regressing on spread and total specifically instead of points)
Step 9) bigboyTrainTestSplit.py creates a training set of the data from 2003-2017 and a test set of the data from 2018 and 2019
