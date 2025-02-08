

''' Functions for games and stats '''


import os
import sys
sys.path.insert(1, "./")

import pickle
import numpy as np
import pandas as pd
from flask import session
from datetime import datetime, timedelta

from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *
from Gamebook.src.my_fun import *




###############################################
#                     GENERAL 
###############################################


# GENERAL

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


def create_random_group():

    group = My_Group(name='random', 
        key='random', 
        players=session['random_players'], 
        colors=[c[0]for c in player_colors],
        slogan ='This is a small test version of the gamebook. Enjoy!')

    return group




###############################################
#                     ROUNDS 
###############################################

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
        session['round'] = 0
        session['game_id'] = game_id
        session['num_players'] = len(players)

        
        # delete open rounds game if no winner_name
        drop_game_id = results[(results['g_mode']=='rounds') \
            & (results['winner_name']=='')].game_id.values
        
        group.results = results.drop(results[results['game_id'].isin(drop_game_id)].index)
         
        
        # group.results  > save in group
        result = { \
            'game_id':game_id, 'g_mode': 'rounds', "group_id":group.id, 
            "result":[points], "n_rounds": 0, 
            "winner_name":'', 'time':datetime.now(),
            'info_1':form.r_title.data, 'info_2': players, 'info_3':''}
        
        group.results = pd.concat([group.results, pd.DataFrame([result])])
        group.update_group()
    
    return game_id, info
          
        

def end_rounds(group, points, game_id, title, players, comment):

    winner = players[np.argmax(points[-1])]
          
    result = {'game_id': game_id, 'g_mode': 'rounds', "group_id": group.id, 
         "result": points, "n_rounds": points.shape[0] - 1, 
         "winner_name": winner, 'time': datetime.now(),
         'info_1': title, 'info_2': players, 'info_3': comment}
    
    for col in result.keys():
        print(col, result[col])
    
    # save in group
    group.results.drop(group.results[group.results['game_id'] == game_id].index, inplace=True)
    group.results = pd.concat([group.results, pd.DataFrame([result])], ignore_index=True)
    group.update_group()
    
    # save in all results
    results = pd.read_csv(f'{path_data}modes/results.csv')
    results = pd.concat([results, pd.DataFrame([result])])
    results.to_csv(f'{path_data}modes/results.csv', index=False)
    
    
   
def create_rounds_chart(points, player_ids):
    
    n = points.shape[0] - 1
    if n < 2:
        chart_data = np.zeros((len(player_ids), 1))
    else:
        chart_points = np.transpose(points[:-1])
        chart_points = np.cumsum(np.array(chart_points), axis=1)
        chart_data = [[r for r in range(1, n + 1)],
                    chart_points.tolist()]
    
    return chart_data
    
    
    
def gen_rounds_logs(id):
    
    group = load_group(id)[0]
    logs = []
    results = group.results[group.results['g_mode']=='rounds'] 
    results = results[results['winner_name'] != '']
    winner_chart = np.zeros((group.n, 2)).astype(int)
    
    # logs with all games played
    for i in range(len(results)):
        
        result = results.iloc[i]
        sums = [str(p) for p in result.result[-1]]
        
        # cols: 0:id, 1:date , 2:winner name, 3:title of game, 
        #       4:players, 5:rounds, 6:comment, 7:color of winner,
        #       8:points per player
        log = [ result.game_id,
                result.time.strftime("%d/%m/%y"), 
                group.players[result.winner_name], 
                result.info_1, 
                ', '.join([group.players[p] for p in result.info_2]),   
                result.n_rounds, 
                result.info_3,
                group.colors[result.winner_name],
                ' : '.join(sums)]
        logs.append(log)
    
    # winner chart
    if len(logs) > 2:
        colors_faint = [group.colors[p] + '69' for p in range(group.n)]
        
        for p in range(group.n):
            n_played = np.sum([p in r for r in results.info_2])
            n_won = np.sum([p == r.winner_name for i, r in results.iterrows()])
            winner_chart[p] = [n_won, n_played - n_won]
        
        win_rates = [f"{round(100 * w / (w + l))}%" for w, l in winner_chart]    
        winner_chart = winner_chart.T.tolist()
        height = str(group.n * 30 + 200) + 'px'
        
        winner_chart = [winner_chart, [group.colors, colors_faint], height, win_rates]
        
    return logs, winner_chart




###############################################
#                     PUZZLES 
###############################################



def gen_puzzle_logs(id):
    
    group = load_group(id)[0]
    logs = []
    results = group.results[group.results['g_mode']=='puzzle'] 
    
    for i in range(len(results)):
        result = results.iloc[i]
        
        # 0:date, 1:winner, 2:puzzle, 3:pcs, 4:time, 5:comment
        log = [result.time.strftime("%d/%m/%y"), 
               group.players[result.winner_name],  
               result.info_1, 
               result.n_rounds, 
               str(timedelta(seconds=result["result"])),
               result.info_3]
        logs.append(log)
    
    return logs

    
    
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
    
    result = {'game_id': game_id, 'g_mode': 'puzzle', "group_id": id, 
         "result": duration, "n_rounds": pcs, 
         "winner_name": player_index, 
         'time': datetime.now(),
         'info_1': puzzle_id, 'info_2': '', 'info_3': form.comment.data, }

    
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
        
        df_results = df_results[df_results['info_1'] != puzzle_id]
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




###############################################
#                     DICE 
###############################################


def check_dice_points(points, round):
    checks = np.full(points.shape, True)
    
    for i in range(6):
        vals = [(i+1)*j for j in range(6)]
        checks[i] = [p in vals or np.isnan(p) for p in points[i]]
        
    for i in [6, 7, 12]:
        checks[i] = [(5 <= p <= 30 or np.isnan(p) or p == 0) \
            for p in points[i]]
    
    for i, v in [[8, 25], [9, 30], [10, 40], [11, 50]]:
        checks[i] = [(p in[v, 0]) or np.isnan(p) for p in points[i]]
    
    counts = np.sum(np.isnan(points), axis=0)
    print(counts, round, (counts == round - 1).all())
    check = (checks == True).all() and (counts == 14 - round).all()
  
    return check, checks



def dice_update_points(points, inputs):
    
    counter = 0
    for r in range(13):
        for p in range(points.shape[1]):
            if np.isnan(points[r, p]):
                if inputs[counter] != None:
                    points[r, p] = inputs[counter]
                counter += 1
                
    return points


def totals_dice(points):
    n = points.shape[1]
    top = np.sum(points[:6], axis=0)
    bottom = np.sum(points[6:], axis=0)
    bonus = np.zeros(n)
    for i in range(n):
        if top[i] >= 63:
            bonus[i] = 35
    total = [t + o + b for t, o, b in zip(top, bottom, bonus)]
    totals = np.vstack([top, bonus, bottom, total])
    
    return totals


def end_dice(group_id, game_id, players, points, infos):
    
    group = load_group(group_id)[0]
    totals = totals_dice(points)
    winner = players[np.argmax(totals)]
    result = np.vstack([points, totals])
    
    result = {'game_id':game_id, 'g_mode': 'dice', "group_id":group.id, 
         "result": result, "n_rounds": points.shape[1], 
         "winner_name":winner, 
         'time':datetime.now(),
         'info_1': players, 'info_2': infos[0], 'info_3':''}
    print(result)
    
    # save in group
    group.results = pd.concat([group.results, pd.DataFrame([result])])
    group.update_group()
    
    # save in all results
    results = pd.read_csv(f'{path_data}modes/results.csv')
    results = pd.concat([results, pd.DataFrame([result])])
    results.to_csv(f'{path_data}modes/results.csv', index=False)   
    pass