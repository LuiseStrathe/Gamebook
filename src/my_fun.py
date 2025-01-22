
import os
import sys
sys.path.insert(1, "./")

import pickle
import numpy as np
import pandas as pd
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, url_for, redirect, flash, session
from datetime import datetime

from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *


###############  SYSTEM  ##################


def init_session():
    session['status'] = 'OUT'
    session['username'] = ''
    session['key'] = ''
    session['game_id'] = 0
    session['mode'] = ''
    session['num_players'] = 0
    session['round'] = 0
    
    
def encrypt_key(key):
    
    path = f'{path_data}/server/salt.txt'
    with open(path, "rt") as f:
        salt = str(f.readline())
    
    hash = 65
    salted = key + salt
    for ch in salted:
        hashed = ( hash*281  ^ ord(ch)*987) & 0xFFFFFFFF
    
    return str(hashed)

    
def verify_session():    
    
    if 'status' in session:    
    
        if session['status'] == "IN":
            
            try: session['username']
            except: pass
            
            else: 
                if session['username'] not in ['random', '']:
                    return True
        
    else: 
        init_session()
        
        return False



def page_html(static, force_in_out="no"):
    
    ''' 
    "page" delivers general data into hmtl 
    and is passed on to head.html base.

    0 -     html head file path
    1 -     page title (for html head)
    2 -     group name (or NaN)
    3 -     player colors
    '''
    
    
    page_html = ["__head_out.html", 
                page_titles[static], 
                "NaN",
                player_colors]
    
    if verify_session():    
        
        page_html[0] = "__head_in.html"
        page_html[2] = session['username']
        
    if force_in_out == 'no':
        pass
    
    elif force_in_out == 'in':
        page_html[0] = "__head_in.html"
        
    else:
        page_html[0] = "__head_out.html"
        
    return page_html



###############  GROUP  ##################



def load_group(id):
    
    path = f'{path_data}groups/{id}.pkl'
    
    if f'{id}.pkl' not in os.listdir(f'{path_data}groups/'):
        success = False
        group = None
    
    else:
        success = True
        with open(path, "rb") as f:
            group = pickle.load(f)
    
    return group, success


def delete_group(id):
    
    path = f'{path_data}groups/{id}.pkl'
    os.remove(path)
    
    init_session()


def name_to_id(name):
    
    for c in ' .,;:!?-':
        name = name.replace(c, '_')
    
    id = name.lower()
    
    return id


def id_to_name(id):
    
    group = load_group(id)[0]
    
    return group.name


def check_name(name):
    
    id = name_to_id(name)
    if id == 'random':
        check = False
    else:
        check = id not in os.listdir(f'{path_data}groups/')
    
    return check, id


def check_key(id, key):

    if id in ['random', '', None]:
            check = False
          
    elif load_group(id)[1] == False:
        check = False
        print('Group not found')
    
    else: 
        check = load_group(id)[0].key == key

    return  check


def create_players(group_form):

    inputs = [ 
        [group_form.p0.data, group_form.c0.data],
        [group_form.p1.data, group_form.c1.data],
        [group_form.p2.data, group_form.c2.data],
        [group_form.p3.data, group_form.c3.data],
        [group_form.p4.data, group_form.c4.data],
        [group_form.p5.data, group_form.c5.data],
        [group_form.p6.data, group_form.c6.data],
        [group_form.p7.data, group_form.c7.data],
        [group_form.p8.data, group_form.c8.data],
        [group_form.p9.data, group_form.c9.data]
    ]
    
    inputs = inputs[:group_form.num.data]
                
    players =   [i[0] for i in inputs if i[0] != '']
    colors =    [i[1] for i in inputs if i[0] != '']

    return players, colors






###############  PLAY  ##################


def gen_game_id(mode):
    
    with open(f'data/max_id.txt', "rt") as f:
        new_id = int(f.readline()) + 1
        print(f'New game id: {new_id}')

    with open(f'data/max_id.txt', "wt") as f:  
        f.write(str(new_id))

    return str(mode_key[mode] + '_' + str(new_id).zfill(10)) 


def create_random_group():

    group = My_Group(name='random', 
        key='random', 
        players=session['random_players'], 
        colors=[c[0]for c in player_colors],
        slogan ='This is a small test version of the gamebook. Enjoy!')

    return group



# ROUNDS


def end_rounds(group, points, game_id, infos):

    winner = group.players[np.argmax(points[-1])]
    print('winner: ', winner)
          
    result = {'game_id':game_id, 'g_mode': 'rounds', "group_id":group.id, 
         "result":points, "n_rounds":points.shape[0], 
         "winner_name":winner, 'time':datetime.now(),
         'info_1':infos[0], 'info_2': infos[1], 'info_3':infos[2]}
    print(result)
    
    # save in group
    group.results = pd.concat([group.results, pd.DataFrame([result])])
    group.update_group()
    
    # save in all results
    results = pd.read_csv(f'{path_data}modes/results.csv')
    results = pd.concat([results, pd.DataFrame([result])])
    results.to_csv(f'{path_data}modes/results.csv', index=False)
    
    


# PUZZLES

    
def add_puzzle(group_id, add_puzzle_form):
    
    group = load_group(group_id)[0]
    
    record = {'id': int(group.puzzles.shape[0]),
                     'title': add_puzzle_form.title.data, 
                     'pcs': add_puzzle_form.pcs.data, 
                     'description': add_puzzle_form.description.data}

    group.puzzles = pd.concat([group.puzzles, 
                               pd.DataFrame([record])])

    group.update_group()
    pass



def submit_puzzle_record(group_id, puzzle_id,
                         puzzle_record_form):
    
    group = load_group(group_id)[0]
    game_id = gen_game_id('puzzle')
    duration =  puzzle_record_form.hours.data * 60^2 \
                + puzzle_record_form.minutes.data * 60 \
                + puzzle_record_form.seconds.data
    pcs = group.puzzles.iloc[puzzle_id, 3]
    
    result = {'game_id':game_id, 'g_mode': 'puzzle', "group_id":group.id, 
         "result": duration, "n_rounds": pcs, 
         "winner_name":puzzle_record_form.player.data[0], 
         'time':datetime.now(),
         'info_1':puzzle_record_form.comment.data, 'info_2': '', 'info_3':''}
    print(result)
    
    # save in group
    group.results = pd.concat([group.results, pd.DataFrame([result])])
    group.update_group()
    
    # save in all results
    results = pd.read_csv(f'{path_data}modes/results.csv')
    results = pd.concat([results, pd.DataFrame([result])])
    results.to_csv(f'{path_data}modes/results.csv', index=False)    
    pass



# DICE


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