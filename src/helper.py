
import os
import sys
sys.path.insert(1, "./")

import pickle
import numpy as np
import pandas as pd
from flask import session

from src.my_params import *


######### CLASSES #########

class Group():

    def __init__(self, name, key, players, motto=None):

        self.name = name
        self.id = name_to_id(name)
        self.players = players
        self.n = len(players)
        self.key = key
        self.games = pd.DataFrame(columns=result_cols)
        self.motto = motto
        self.filepath = f'{path_data}groups/{self.id}.pkl'

        try:
            check_name(self.name)
        except:
            print('Please check your group name and key.')

        try:
            with open(self.filepath, "wb") as f:
                pickle.dump(self, f)
        except:
            print('This name already exists. Please choose another one.')

    def update_group(self):
        with open(self.filepath, "wb") as f:
            pickle.dump(self, f)


######### FUNCTIONS #########

def init_session():
    session['status'] = 'OUT'
    session['username'] = ''
    session['key'] = ''
    session['game_id'] = 0
    session['mode'] = ''
    session['num_players'] = 0


def load_group(id):
    print(f'Loading group w/ id = {id}')
    path = f'{path_data}groups/{id}.pkl'
    print('path = ', path)
    with open(path, "rb") as f:
        group = pickle.load(f)
    return group


def delete_group(id):
    path = f'{path_data}groups/{id}.pkl'
    os.remove(path)


def name_to_id(name):
    for c in ' .,;:!?':
        name = name.replace(c, '-')
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

def gen_game_id():
    
    with open(f'data/max_id.txt', "rt") as f:
        new_id = int(f.readline()) + 1
        print(f'New game id: {new_id}')
    with open(f'data/max_id.txt', "wt") as f:  
        f.write(str(new_id))
        
    return new_id


def create_random_group(n):
    players = [f'Player {i+1}' for i in range(n)]
    group = Group(name='random', key='random', players=players)
    return group