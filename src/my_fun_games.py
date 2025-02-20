

''' Functions for games and stats '''


import os
import sys
sys.path.insert(1, "./")

import pickle
import numpy as np
import pandas as pd
import json
from flask import session
from datetime import datetime, timedelta, time

from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *
from Gamebook.src.my_fun import *




###############################################
#                     GENERAL 
###############################################



def gen_game_id(mode):
    
    # mode-index
    mode_idx = modes.index(mode)
    
    with open(f'data/max_id.txt', "rt") as f:
        ids = [int(i) for i in f.readline().split(sep=',')]
        
    new_id = ids[mode_idx] + 1
    ids[mode_idx] = new_id
    ids = ','.join([str(i) for i in ids])

    with open(f'data/max_id.txt', "wt") as f:  
        f.write(ids)

    return str(mode_key[mode] + str(new_id).zfill(10)) 



def winner_str(players, winner_ids):
    
    if winner_ids == '' or winner_ids == None:
        return ''
    
    if type(winner_ids) == int:
        return players[winner_ids]
    
    return ' & '.join([players[id] for id in winner_ids])



###############################################
#                     ROUNDS 
###############################################



# start from GROUP page

def start_rounds(group_id, form):
          
    # check players
    group = load_group(group_id)[0]
    players = [p for p in range(group.n) if form[f'r_p_{p}'].data]
            
    if len(players) < 2:
        info = 'Select at least 2 players for a rounds game.'
        game_id = 0
        
    else:
        # init game
        info = ''
        game_id = gen_game_id('rounds')
        points = np.zeros((1, len(players)))  
        group = load_group(group_id)[0]
        results = group.results

        
        # delete open rounds game if no winner_name
        drop_game_id = results[(results['mode']=='rounds') \
            & (results['winner_id']=='')].game_id.values
        
        print('\n  drop_game_id\n', drop_game_id)
        group.results = results.drop(results[results['game_id'].isin(drop_game_id)].index)
         
        
        # group.results  > save in group
        result = { \
            'game_id': game_id, 'mode': 'rounds', 'group_id': group.id, 'time_stamp': datetime.now(),
            'g_data': [points], 'n_rounds': 0, 'title': form.r_title.data,
            'player_ids': players, 'winner_id': '', 'comment': '',
            'info_1': '', 'info_2': '', 'info_3': ''}
        
        
        group.results = pd.concat([group.results, pd.DataFrame([result])])
        group.update_group()        
        
    return game_id, info
          
   

# CREATE data to display  

def gen_rounds_stats(id):
    
    group = load_group(id)[0]
    logs = []
    results = group.results[group.results['mode']=='rounds'] 
    results = results[results['winner_id'] != '']
    winner_chart = np.zeros((group.n, 2)).astype(int)
    
    # logs with all games played
    for i in range(len(results)):
        
        result = results.iloc[i]
        sums = [str(p) for p in result.g_data[-1]]
        if len(result.winner_id) > 1:
            color_css = 'background-image: linear-gradient(to right, ' + \
                'c9, '.join([group.colors[p] for p in result.winner_id])\
                + 'c9);'
        else:
            color_css = 'background-color: ' + group.colors[result.winner_id[0]] + 'c9;'
        
        # cols: 0:id, 1:date , 2:winner name, 3:title of game, 
        #       4:players, 5:rounds, 6:comment, 7:color of winner,
        #       8:points per player
        log = [ result.game_id,
                result.time_stamp.strftime("%d/%m/%y"), 
                winner_str(group.players, result.winner_id),
                result.title, 
                ', '.join([group.players[p] for p in result.player_ids]),   
                result.n_rounds, 
                result.comment,
                color_css,
                ' : '.join(sums)
                ]
        logs.insert(0, log)
    
    # winner chart
    if len(logs) > 2:
        colors, colors_faint, log_names = [], [], []
        log_players = np.zeros(group.n, dtype=int)
        
        for p in range(group.n):
            n_played = np.sum([p in r for r in results.player_ids])
            if n_played > 0:
                n_won = np.sum([p in r.winner_id for i, r in results.iterrows()])
                winner_chart[p] = [n_won, n_played - n_won]
                log_players[p] = 1
                log_names.append(group.players[p])
                colors.append(group.colors[p])
                colors_faint.append(group.colors[p] + '30')

        winner_chart = winner_chart[log_players == 1]
        win_rates = [f"{round(100 * w / (w + l)) if w + l > 0 else 'n/a'}%" for w, l in winner_chart if w + l > 0]
        height = str(sum(log_players) * 30 + 200) + 'px'
        
        winner_chart = winner_chart.T.tolist()
        winner_chart = [winner_chart, log_names, [colors, colors_faint], height, win_rates]
        
    return logs, winner_chart



def create_rounds_chart(points, player_ids):
    
    round = points.shape[0] - 1
    
    if round < 2:
        chart_data = np.zeros((len(player_ids), 1))
        
    else:        
        chart_points = np.transpose(points[:-1])
        chart_points = np.cumsum(np.array(chart_points), axis=1)
        chart_data = [[r for r in range(1, round + 1)],
                    chart_points.tolist()]
        
    return chart_data



# during PLAYING

def next_rounds(group, game_id, result, points, n, form, n_players):
    info = ''
    
    # get new input points
    new_points = [form[f"pt{str(i)}"].data for i in range(n_players)]
    if None in new_points:
        info = 'Enter points for all players.'
        return info
    
    new_points = [int(p) if p != None else 0 for p in new_points]
    new_points = np.array(new_points, dtype=int)
    
    
    # merge with existing points
    if n == 0: 
        points = np.vstack([new_points, new_points])
    
    else: 
        # remove & add total row  
        points = np.vstack([points[:-1], new_points])          
        points = np.vstack([points, np.sum(points, axis=0)])   

    
    # update group
    result.g_data= [points]
    result.n_rounds = n + 1   
    group.results[group.results.game_id == game_id] = result
    group.update_group()
    
    return info
    


def end_rounds(group, points, game_id, title, players, comment):

    win_points = max(points[-1])
    winners = [players[p] for p in range(len(players)) if points[-1, p] == win_points]
          
    result = {'game_id': game_id, 'mode': 'rounds', 'group_id': group.id, 'time_stamp': datetime.now(), 
         'g_data': points, "n_rounds": points.shape[0] - 1, 'title': title, 
         'player_ids': players, 'winner_id': winners, 'comment': comment,
         'info_1': '', 'info_2': '', 'info_3': ''}
    
    
    # save in group
    results = group.results.copy().reset_index(drop=True)
    drop_index = results[results.game_id == game_id].index
    results = results.drop(drop_index)
    
    results = pd.concat([results, pd.DataFrame([result])], ignore_index=True)
    group.results = results
    group.update_group()
    
    # save in all results
    results = pd.read_csv(f'{path_data}modes/results.csv')
    results = pd.concat([results, pd.DataFrame([result])])
    results.to_csv(f'{path_data}modes/results.csv', index=False)
    
    pass







###############################################
#                     DICE 
###############################################



# start from GROUP page

def start_dice(group_id, form):
          
    # VERIFY
    group = load_group(group_id)[0]
    player_ids = [p for p in range(group.n) if form[f'd_p_{p}'].data]
    n_players = len(player_ids)
            
    if len(player_ids) < 2:
        info = 'Select at least 2 players for a dice game.'
        game_id = 0
    
    
    # INIT GAME
    else:
        info = ''
        game_id = gen_game_id('dice')
        group = load_group(group_id)[0]
        results = group.results
        
        # 0:points      - 17 = 13 game + 4 sum rows
        # 1:history     - 13 rounds
        # 2:activation  - 13 rounds; 0 = input field, 1 = data given
        
        points = np.empty((17, n_players), dtype=object)
        points[-4:] = np.zeros((4, n_players), dtype=int)
        history = np.zeros((13, n_players), dtype=int)
        activation = np.zeros((13, n_players), dtype=bool)
        
        
        # delete open dice game if no winner_name
        drop_game_id = results[(results['mode']=='dice') \
            & (results['winner_id']=='')].game_id.values
        
        group.results = results.drop(results[results['game_id'].isin(drop_game_id)].index)
         
        
        # SAVE game data in group
        result = { \
            'game_id': game_id, 'mode': 'dice', "group_id": group.id, 'time_stamp': datetime.now(),
            'g_data': [points, history, activation], 'n_rounds': 0, 'title': '', 
            'player_ids': player_ids, 'winner_id': [], 'comment': '',
            'info_1': '', 'info_2': '', 'info_3':''}
        
        group.results = pd.concat([group.results, pd.DataFrame([result])])
        group.update_group()
        
    return game_id, info



# CREATE data to display

def gen_dice_stats(id):
    
    group = load_group(id)[0]
    logs = []
    results = group.results[group.results['mode']=='dice'] 
    results = results[results['n_rounds'] == 14]
    winner_chart = np.zeros((group.n, 2)).astype(int)
    
    # logs with all games played
    for i in range(len(results)):
        
        result = results.iloc[i]
        sums = [str(p) for p in result.g_data[0][-1]]
        winner_ids = result.winner_id

        if len(winner_ids) > 1:
            color_css = 'background-image: linear-gradient(to right, ' + \
                'c9, '.join([group.colors[p] for p in winner_ids])\
                + 'c9);'
        else: 
            color_css = 'background-color: ' + group.colors[winner_ids[0]] + 'c9;'
        
        # cols: 0:id, 1:date , 2:winner name, 3:title of game, 
        #       4:players, 5:rounds, 6:comment, 7:color of winner,
        #       8:points per player
        log = [ result.game_id,
                result.time_stamp.strftime("%d/%m/%y"), 
                winner_str(group.players, winner_ids),
                result.title, 
                ', '.join([group.players[p] for p in result.player_ids]),   
                result.n_rounds, 
                result.comment,
                color_css,
                ' : '.join(sums)
                ]
        logs.insert(0, log)
    
    # winner chart
    if len(logs) > 2:
        colors, colors_faint, log_names = [], [], []
        log_players = np.zeros(group.n, dtype=int)
        
        for p in range(group.n):
            n_played = np.sum([p in r for r in results.player_ids])
            if n_played > 0:
                n_won = np.sum([p in r.winner_id for i, r in results.iterrows()])
                winner_chart[p] = [n_won, n_played - n_won]
                log_players[p] = 1
                log_names.append(group.players[p])
                colors.append(group.colors[p])
                colors_faint.append(group.colors[p] + '30')

        winner_chart = winner_chart[log_players == 1]
        win_rates = [f"{round(100 * w / (w + l)) if w + l > 0 else 'n/a'}%" for w, l in winner_chart if w + l > 0]
        height = str(sum(log_players) * 30 + 200) + 'px'
        
        winner_chart = winner_chart.T.tolist()
        winner_chart = [winner_chart, log_names, [colors, colors_faint], height, win_rates]
        
    return logs, winner_chart



def create_dice_point_entries(game_data, round, form, n_players):
    
    points, history, activation = game_data.copy()
    point_entries = points        # if 13: finished
    
    if round == 0:                          # game started
        for row in range(13):
            row_id = dice_rows[0][row]
            for p in range(n_players):
                point_entries[row, p] = form[f"p{p}_{row_id}"]()
        
    elif round < 13:                        # game in progress
        for row in range(13):
            row_id = dice_rows[0][row]
            for p in range(n_players):
                if not activation[row, p]:
                    point_entries[row, p] = form[f"p{p}_{row_id}"]()

    return point_entries.tolist()



def create_dice_game_chart(history):
    chart_data = [[r for r in range(1, 14)], history.T.tolist()]
    return chart_data



# during PLAYING

def next_dice(group, game_id, game_data, form):

    info = ''
    points, history, activation = game_data.copy()
    n_players = points.shape[1]
    round = np.sum(activation) / n_players
    
    # check new data 
    new_points, new_activation = dice_update_points(points, activation, form, n_players)
    info = check_dice_points(new_points, new_activation, n_players)
    
    # update group
    if info == '':
        
        new_points = update_totals_dice(new_points)
        history = dice_history(history, new_points, activation, new_activation, n_players)
        round = np.sum(new_activation) / n_players
        
        result = group.results[group.results.game_id == game_id].copy()
        result.n_rounds = round
        result.loc[0, 'g_data'][:] = [new_points, history, new_activation]
        
        if round == 13:
            win_points = max(new_points[-1])
            winners = [result.player_ids[0][p] for p in range(points.shape[1]) if new_points[-1, p] == win_points]
            #result.winner_id[0] = winners
            if type(winners) == int:
                result.loc[0, 'winner_id'] = winners
            else:
                result.winner_id[0] = winners 
            result.loc[0, 'time_stamp'] = datetime.now()
            result.loc[0, 'n_rounds'] = 13
        
        group.results[group.results.game_id == game_id] = result
        
        group.update_group()
    
    return info



def dice_update_points(points, activation, form, n_players):
    
    new_points, new_activation = points.copy(), activation.copy()
    
    for row in range(13):
        row_id = dice_rows[0][row]
        for p in range(n_players):
            if not activation[row, p] and form[f"p{p}_{row_id}"].data != None:
                new_points[row, p] = int(form[f"p{p}_{row_id}"].data)
                new_activation[row, p] = True
                
    return new_points, new_activation



def check_dice_points(points, new_activation, n_players):
    
    info = ''       # '' if all good, else error message
    
    # full round
    player_activations = np.sum(new_activation, axis=0)
    
    if len(set(player_activations)) != 1 :
        return "Forgot someone? Players have to have the same number of values entered."
    
    
    for row in range(13):
        for p in range(n_players):
            if new_activation[row, p]:
                point = points[row, p]
                
                # not negative
                if point < 0:
                    return f"Points can't be negative ({point})."
                
                # not over 30 in top, kinds and chance
                elif (row in range(8) or row == 12) and point > 6 * 5:
                    return f"This value can't be over 30, you entered {point}."
                
                # i's multiples in 1 to 6
                elif row < 6 and point not in [(row + 1) * i for i in range(0, 6)]:
                    return f"{row + 1}'s must be a multiple of {row + 1}. You entered {point}."
                
                # 3 & 4 of a kind
                elif row in [6, 7]:
                    if point in [1, 2, 3, 4]:
                        return f'This value is not possible for {row - 3} of a kind: {point}.'  
                    
                # full house
                elif row == 8 and point not in [25, 0]:
                    return f'This value is not possible for full house: {point}.'
                
                # small & large straight
                elif row == 9 and point not in [30, 0]:
                    return f'A small straight can be 0 or 30 points, not {point}.'
                elif row == 10 and point not in [40, 0]:
                    return f'A large straight can be 0 or 40 points, not {point}.'
                
                # gamer
                elif row == 11 and point not in [50, 0]:
                    return f'A gamer can be 0 or 50 points, not {point}.'
            
                # chance
                elif row == 12:
                    if point in [1, 2, 3, 4]:
                        return f'This value is not possible for chance: {point}.'
  
    return ''   # all good



def update_totals_dice(points):
    
    n = points.shape[1]
    orig_points = points.copy()
    points[points == None] = 0
    
    top = np.sum(points[:6], axis=0)
    bottom = np.sum(points[6:13], axis=0)
    bonus = np.zeros(n, dtype=int)
    
    for i in range(n):
        if top[i] >= 63:
            bonus[i] = 35
            
    total = [t + o + b for t, o, b in zip(top, bottom, bonus)]
    totals = np.vstack([top, bonus, bottom, total])
    orig_points[-4:] = totals
    
    return orig_points



def dice_history(history, new_points, activation, new_activation, n_players):

    added_activation = np.logical_xor(activation, new_activation)
    prior_rounds = np.sum(activation, axis=0)[0]
    new_history = history.copy()
     
     
    for p in range(n_players):
        counter = 0
        for r in range(13):
            if added_activation[r, p]:
                
                line_history = counter + prior_rounds
                prior_history = new_history[line_history - 1, p] if line_history > 0 else 0
                new_history[line_history, p] = new_points[r, p] + prior_history
                counter += 1
    
    return new_history


# FINISH game

def end_dice(group, game_id, player_ids, game_data, winner_ids, comment):
    
    points, history, activation = game_data
    points = update_totals_dice(points)
    game_data = [points, history, []]
    
    result = {
        'game_id': game_id, 'mode': 'dice', 'group_id': group.id, 'time_stamp': datetime.now(), 
        'g_data': game_data, 'n_rounds': 14, 'title': '',        # round=14 > to indicate finished game
        'player_ids': player_ids, 'winner_id': winner_ids, 'comment': comment,
        'info_1': '', 'info_2': '', 'info_3': ''}
    
    # save in group
    group = load_group(group.id)[0]
    
    results = group.results.copy().reset_index(drop=True)
    drop_index = results[results.game_id == game_id].index
    results = results.drop(drop_index)
    
    group.results = pd.concat([results, pd.DataFrame([result])], ignore_index=True)
    group.update_group()
    
    # save in all results

    results = pd.read_csv(f'{path_data}modes/results.csv')
    results = pd.concat([results, pd.DataFrame([result])])
    results.to_csv(f'{path_data}modes/results.csv', index=False)   
    
    pass







###############################################
#                     PUZZLES 
###############################################




# PUZZLES page

def add_puzzle(group_id, add_puzzle_form):
    
    group = load_group(group_id)[0]
    info = ''
    
    # avoid 0 & add 1 new puzzle with id n:
    n = int(group.puzzles.shape[0]) + 1 
    
    if add_puzzle_form.title.data not in group.puzzles.title.values:
        
        record = {
            'id': n,
            'title': add_puzzle_form.title.data, 
            'pcs': add_puzzle_form.pcs.data, 
            'description': add_puzzle_form.description.data}

        group.puzzles = pd.concat([group.puzzles, 
                                pd.DataFrame([record])])

        group.update_group()
        info = ""
        
    else:
        info = f"Puzzle {add_puzzle_form.title.data} already exists."
    
    return info



def submit_puzzle_record(id, form):
    
    group = load_group(id)[0]
    game_id = gen_game_id('puzzle')        
    duration =  form.hours.data * 60 * 60 \
                + form.minutes.data * 60 \
                + form.seconds.data
    puzzle_id = int(form.puzzle.data.split(':')[0])
    pcs = group.puzzles.pcs.iloc[puzzle_id - 1]
    player_index  = group.players.index(form.player.data)
    
    result = {
        'game_id': game_id, 'mode': 'puzzle', "group_id": id, 'time_stamp': datetime.now(),
        'g_data': duration, 'n_rounds': pcs, 'title': puzzle_id, 
        'player_ids': '', 'winner_id': player_index, 'comment': form.comment.data,
        'info_1': '', 'info_2': '', 'info_3': '', }

    
    # save in group
    group.results = pd.concat([group.results, pd.DataFrame([result])], ignore_index=True)
    group.update_group()
    
    # save in all results
    results = pd.read_csv(f'{path_data}modes/results.csv')
    results = pd.concat([results, pd.DataFrame([result])])
    results.to_csv(f'{path_data}modes/results.csv', index=False)    
    
 
    
def change_puzzle(id, form):
    
    group = load_group(id)[0]
    puzzle_id = int(form.puzzle_change.data.split(':')[0])
    df_puzzles = group.puzzles
    df_results = group.results
    

    if form.delete.data:
        
        df_puzzles = df_puzzles[df_puzzles['id'] != puzzle_id]
        
        df_results = df_results[df_results['title'] != puzzle_id]
        group.results = df_results
        
        
    else:
        if form.title_change.data not in [None, '']:
            df_puzzles.title.iloc[puzzle_id - 1] = form.title_change.data
            
        if form.description_change.data not in [None, '']:
            df_puzzles.description.iloc[puzzle_id - 1] = form.description_change.data

            
    # update id
    df_puzzles['id'] = range(1, df_puzzles.shape[0] + 1)
    
    group.puzzles = df_puzzles 
    group.update_group()
    pass



def gen_puzzle_logs(id):
    
    group = load_group(id)[0]
    logs = []
    results = group.results[group.results['mode']=='puzzle'] 
    
    for i in range(len(results)):
        result = results.iloc[i]
        
        # 0:date, 1:winner, 2: color, 3:puzzle, 4:pcs, 5:time, 6:comment
        log = [result.time_stamp.strftime("%d/%m/%y"), 
                group.players[result.winner_id],  
                group.colors[result.winner_id],   
                result.title, 
                result.n_rounds, 
                str(timedelta(seconds=result["g_data"])),
                result.comment]
        logs.insert(0, log)
    
    return logs



# STATS page

def gen_puzzle_charts(logs, puzzle_names, chart_colors): 
      
    # clean logs
    logs = [l for l in logs if l[5] != '0:00:00']
  
    
    # LABELS 
    categories = sorted(list(set([l[4] for l in logs])), reverse=False)
    players = list(set([l[1] for l in logs]))
    puzzles = sorted(list(set([l[3] for l in logs])))

    
    # DATA
    logged = np.zeros((len(players), len(categories)), dtype=int)
    times_player = np.zeros((len(players), 2, len(categories)), dtype=float)
    times_puzzle = np.zeros((len(puzzles), 2, len(categories)), dtype=float)
    avg_player, avg_puzzle = [], []

    
    # player data
    for p in range(len(players)):
        playr = players[p]
        log_p = [l for l in logs if l[1] == playr]
        
        times = [l[5].split(':') for l in log_p]
        times = [int(s) / 60 + int(m) + 60 * int(h) for h, m, s in times]
        pieces = np.sum([l[4] for l in log_p])
        avg = np.sum(times) / pieces
        avg_player.append(round(avg, 2))
            
        for c in range(len(categories)):
            cat = categories[c]
            log = [l for l in log_p if l[4] == cat]
            
            logged[p, c] = len(log)
            
            times = [l[5].split(':') for l in log]
            times = [int(s) / 60 + int(m) + 60 * int(h) for h, m, s in times]

            if len(times) > 0:
                avg = cat / np.mean(times)
                top = cat / np.min(times)
                times_player[p, 0, c] = round(avg, 1)
                times_player[p, 1, c] = round(top, 1)
        
        logged[c] = logged[c].tolist()
        
        
        
        
    # puzzle data
    
    for z in range(len(puzzles)):
        puz = puzzles[z]
        log_z = [l for l in logs if l[3] == puz]
        
        times = [l[5].split(':') for l in log_z]
        times = [int(s) / 60 + int(m) + 60 * int(h) for h, m, s in times]
        pieces = np.sum([l[4] for l in log_z])
        avg = np.sum(times) / pieces
        avg_puzzle.append(round(avg, 2))
        
        for c in range(len(categories)):
            cat = categories[c]
            log = [l for l in log_z if l[4] == cat]
            
            times = [l[5].split(':') for l in log]
            times = [int(s) / 60 + int(m) + 60 * int(h) for h, m, s in times]
            
            if len(times) > 0:
                avg = cat / np.mean(times)
                top = cat / np.min(times)
                
                times_puzzle[z, 0, c] = round(avg, 1)
                times_puzzle[z, 1, c] = round(top, 1)
                
            else:
                times_puzzle[z, :, c] = [None, None]
                
        


    # EXTRA data
    
    colors, colors_puzzles = [], []
        
    categories = ['# ' + str(cat) for cat in categories]
    
    sum_logged = [int(np.sum(logged[p])) for p in range(len(players))]  
    
    while len(puzzles) > len(chart_colors):
        chart_colors += chart_colors        
        
        
    for p in players:
        
        color, i = "", 0
        while color == '' and i < len(logs):
            if logs[i][1] == p:
                color = logs[i][2]
            i += 1
        colors.append([color, color + '30'])
    
    
    for z in range(len(puzzles)):
        
        puzzles[z] = puzzle_names['title'][puzzle_names['id'] == puzzles[z]][0]
        
        color = chart_colors[z]
        colors_puzzles.append([color, color + '30'])
  
                
    # COMBINE DATA
    charts = [
        [categories, players, colors, puzzles, colors_puzzles],
        [sum_logged, avg_player, avg_puzzle], 
        [logged.tolist(), times_player.tolist(), json.dumps(times_puzzle.tolist())]]
    
    return charts

    
    

