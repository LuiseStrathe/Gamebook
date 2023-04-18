
import os
import sys
sys.path.insert(1, "./")

import pickle
import numpy as np
import pandas as pd
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, url_for, redirect, flash, session
from datetime import datetime

from src.my_params import *
from src.my_classes import *



def init_session():
    session['status'] = 'OUT'
    session['username'] = ''
    session['key'] = ''
    session['game_id'] = 0
    session['mode'] = ''
    session['num_players'] = 0
    session['round'] = 0

def get_base():
    base = '_base.html'
    if session['status'] == 'IN':
        base = '_base_in.html'
    return base

def load_group(id):
    path = f'{path_data}groups/{id}.pkl'
    with open(path, "rb") as f:
        group = pickle.load(f)
    return group


def delete_group(id):
    path = f'{path_data}groups/{id}.pkl'
    os.remove(path)


def name_to_id(name):
    for c in ' .,;:!?-':
        name = name.replace(c, '_')
    id = name.lower()
    return id

def id_to_name(id):
    group = load_group(id)
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
    else: check = load_group(id).key == key
    return  check


def create_players(group_form):
    players = [group_form.p1.data, group_form.p2.data,
               group_form.p3.data, group_form.p4.data]
    players = [p for p in players if p != '']
    return players


def gen_game_id(mode):
    
    with open(f'data/max_id.txt', "rt") as f:
        new_id = int(f.readline()) + 1
        print(f'New game id: {new_id}')
    with open(f'data/max_id.txt', "wt") as f:  
        f.write(str(new_id))

    return str(mode_key[mode] + '_' + str(new_id).zfill(10)) 


def create_random_group():
    group = My_Group(name='random', key='random', players=session['random_players'], motto='random')
    return group


def end_rounds(group, points, game_id, info):
    winner = group.players[np.argmax(points[-1])]
    
    result = {'game_id':game_id, 'mode': game_id[0], "group":group.id, 
         "result":points[-1][:], "n_rounds":points.shape[0], 
         "winner":winner, 'info':info, 'time':datetime.now()}
    
    # save game points
    points.save(f'{path_data}games/{game_id}.npy')
    
    # save in group
    group.results.append(result, ignore_index=True)
    group.update_group()
    
    # save in all results
    results = pd.read_csv(f'{path_data}results.csv')
    results = results.append(result, ignore_index=True)
    results.to_csv(f'{path_data}results.csv', index=False)
    