import pandas as pd

games = pd.read_csv('master_data/odi_ballbyball.csv')
info = pd.read_csv('master_data/odi_info.csv')

# get running total of runs and wickets
def do_cumsums(df):
    df['inn_runs'] = df['total_runs'].cumsum()
    df['inn_wickets'] = df['wicket'].fillna(0).cumsum()
    return df
games_pr = games.groupby(['game_id','innings']).apply(do_cumsums)

# keep only relevant info
games_trim = games_pr[['game_id','innings','batting_side','over_number','ball_in_over','inn_runs','inn_wickets']]
info_trim = info[['game_id','date','match_winner']]

# merge
ball_info = pd.merge(games_trim, info_trim, on = 'game_id', how = 'left')

# make sure games ended
ball_info = ball_info[~ball_info.match_winner.isin(['tie','no result'])]

# figure out if the team batting in that innings won
ball_info['bat_win'] = (ball_info.batting_side == ball_info.match_winner)*1

# create this column to not let extra balls affect number of balls left
ball_info['diff_over_6'] = ball_info[ball_info.ball_in_over > 6].ball_in_over - 6
ball_info.diff_over_6.fillna(0, inplace = True)

# number of balls left
ball_info['balls_left'] = (300 - ball_info['over_number']*6 - ball_info['ball_in_over'] + ball_info['diff_over_6'])

ball_info.drop(['diff_over_6'], axis = 1, inplace = True)

# percent of resources remaining
ball_info['pct_balls_left'] = ball_info.balls_left / 300
ball_info['pct_wickets_left'] = (10-ball_info.inn_wickets)/10

### getting chase count for 2nd innings

# get chase total into data frame
chase_numbers = ball_info[ball_info.innings == '1st innings'].groupby('game_id').inn_runs.max().reset_index()
chase_numbers.columns = ['game_id','chase_total']

# merge chase totals with play by play
balls_w_chase = pd.merge(ball_info, chase_numbers, on = 'game_id', how = 'left')

# clear out 1st innings totals
balls_w_chase.chase_total[balls_w_chase.innings == '1st innings'] = None

# calculate number of runs to chase
balls_w_chase['runs_to_chase'] = balls_w_chase.chase_total - balls_w_chase.inn_runs

# fix
balls_w_chase.runs_to_chase[balls_w_chase.runs_to_chase < 0] = 0

balls_w_chase.to_csv('master_data/odi_ballinfotrim.csv', index = False)