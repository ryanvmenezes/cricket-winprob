import pandas as pd
import glob
import yaml

files = glob.glob('odi-data\*.yaml')

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

infos = []

for f in files:
    with open(f,'r') as gamefile:
        game = yaml.load(gamefile)
    gameid = f[9:15]
    print 'starting game ' + gameid
    info_dict = game['info']
    results = (gameid,) + get_game_info(info_dict)
    infos.append(results)
    

match_info = pd.DataFrame(infos, columns = ['game_id','date','venue','city','neutral','match_type','overs','team_inn1','team_inn2','toss_winner','toss_decision','match_winner','win_type','margin','umpires','man_of_match'])

match_info.to_csv('cricsheet_odi_international_info.csv',index = False)