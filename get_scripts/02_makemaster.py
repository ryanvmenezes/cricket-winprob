import pandas as pd
import glob
import yaml

files = glob.glob('all_odis/*.yaml')

def get_game_info(info_dict):
    start_date = info_dict['dates'][0].strftime('%Y-%m-%d')
    venue = info_dict.get('venue')
    city = info_dict.get('city')
    match_type = info_dict.get('match_type')
    neutral = info_dict.get('neutral_venue',0)
    toss_winner = info_dict['toss']['winner']
    toss_loser = list(set(info_dict['teams']) - set([toss_winner]))[0]
    toss_decision = info_dict['toss']['decision']
    team_inn1 = toss_winner if toss_decision == 'bat' else toss_loser
    team_inn2 = list(set(info_dict['teams']) - set([team_inn1]))[0]
    umpires = '|'.join(info_dict['umpires'])
    if info_dict['outcome'].get('result') is None:
        match_winner = info_dict['outcome']['winner']
        win_type = info_dict['outcome']['by'].keys()[0]
        margin = info_dict['outcome']['by'][win_type]
        man_of_match = '|'.join(info_dict['player_of_match']) if info_dict.get('player_of_match') is not None else None
    else:
        match_winner = info_dict['outcome']['result']
        win_type = None
        margin = None
        man_of_match = None
    overs = info_dict['overs']
    return (start_date, venue, city, neutral, match_type, overs, team_inn1, team_inn2, toss_winner, toss_decision, 
            match_winner, win_type, margin, umpires, man_of_match)

def get_ball_by_ball(innings_obj, game_id):
    all_balls = {}
    for i in range(0,len(innings_obj)):
        key = innings_obj[i].keys()[0]
        all_balls[key] = innings_obj[i][key]
    # all_balls = dict(innings_obj[0].items() + innings_obj[1].items())
    all_info = []
    for innings in all_balls.keys():
        batting_side = all_balls[innings]['team']
        balls = all_balls[innings]['deliveries']
        for b in balls:
            ball_key = b.keys()[0]
            ball_id = str(ball_key).split('.')
            over_number = ball_id[0]
            ball_in_over = ball_id[1]
            ball_details = b[ball_key]
            bowler = ball_details['bowler']
            batsman = ball_details['batsman']
            non_striker = ball_details['non_striker']
            batted_runs = ball_details['runs']['batsman']
            total_extras = ball_details['runs']['extras']
            total_runs = ball_details['runs']['total']
            if ball_details.get('extras') is not None:
                xb = ball_details['extras'].get('byes',None)
                xlb = ball_details['extras'].get('legbyes',None)
                xnb = ball_details['extras'].get('noballs',None)
                xw = ball_details['extras'].get('wides',None)
                xpen = ball_details['extras'].get('penalty',None)
            else:
                xb, xlb, xnb, xw, xpen = (None,) * 5
            non_boundary = ball_details['runs'].get('non_boundary',0)
            if ball_details.get('wicket') is not None:
                wicket = 1
                kind = ball_details['wicket']['kind']
                player_out = ball_details['wicket']['player_out']
                fielders = '|'.join(ball_details['wicket']['fielders']) if bool(ball_details['wicket'].get('fielders')) else None
            else:
                wicket, kind, player_out, fielders = (None,) * 4
            all_info.append((game_id, innings, batting_side, over_number, ball_in_over, bowler, batsman, non_striker,
                batted_runs, xb, xlb, xnb, xw, xpen, total_extras, total_runs, non_boundary, wicket, kind, player_out, fielders))
    return all_info

INFO_COLUMNS = ['game_id','date','venue','city','neutral','match_type','overs','team_inn1','team_inn2','toss_winner','toss_decision','match_winner','win_type','margin','umpires','man_of_match']
GAME_COLUMNS = ['game_id','innings','batting_side','over_number','ball_in_over','bowler','batsman','non_striker','batted_runs','xb','xlb','xnb','xw','xpen','total_extras','total_runs','non_boundary','wicket','kind','player_out','fielders']

info_list = []
allgames_df = pd.DataFrame(None, columns = GAME_COLUMNS)

for f in files:
    with open(f,'r') as gamefile:
        game = yaml.load(gamefile)
    gameid = f[9:15]
    print 'starting game ' + gameid

    # get info
    info_dict = game['info']
    results = (gameid,) + get_game_info(info_dict)
    info_list.append(results)

    # get ball by ball
    ind_game_df = pd.DataFrame(get_ball_by_ball(game['innings'], gameid), columns = GAME_COLUMNS)
    allgames_df = pd.concat([allgames_df, ind_game_df], axis = 0)

match_info = pd.DataFrame(info_list, columns = INFO_COLUMNS)

if not os.path.exists('master_data'):
    os.makedirs('master_data')

match_info.to_csv('master_data/odi_info.csv',index = False)
allgames_df.to_csv('master_data/odi_ballbyball.csv', index = False)