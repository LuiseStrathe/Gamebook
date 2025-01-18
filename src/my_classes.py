
import os
import sys
sys.path.append("./")

import pickle
import numpy as np
import pandas as pd
from flask import session

from Gamebook.src.my_params import *




# helper functions to avoid circular imports

def name_to_id_create(name):
    for c in ' .,;:!?-':
        name = name.replace(c, '_')
    id = name.lower()
    return id


def check_name_create(name):
    id = name_to_id_create(name)
    if id == 'random':
        check = False
    else:
        check = id not in os.listdir(f'{path_data}groups/')
    return check, id




# classes

class My_Group():

    def __init__(self, name, key, players, colors, slogan=None):

        # Create group

        self.name = name
        self.id = name_to_id_create(name)
        self.players = players
        self.colors = colors
        self.player_info = pd.DataFrame(columns=player_cols)
        self.n = len(players)
        self.key = key
        
        self.slogan = slogan
        
        self.filepath = f'{path_data}groups/{self.id}.pkl'
        
        self.results = pd.DataFrame(columns=result_cols)
        self.puzzles = pd.DataFrame(columns=puzzle_cols)

        try:
            check_name_create(self.name)
        except:
            print('Please check your group name and key.')

        try:
            with open(self.filepath, "wb") as f:
                pickle.dump(self, f)
        except:
            print('This name already exists. Please choose another one.')





    # Class methods

    def update_group(self):
        
        with open(self.filepath, "wb") as f:
            pickle.dump(self, f)
            print(f'>> group {self.id} saved')




    def update_settings(self, settings_form):
        
        # slogan
        if settings_form.slogan.data not in ['', None, " "]:
            self.slogan = settings_form.slogan.data
            print(f'>> new slogan: {settings_form.slogan.data}')
            print(f'>> slogan updated: {self.slogan}')
            
        
        for p in range(self.n):           
            
            # existing player
            if settings_form[f'x{p}'].data:
                
                player = [settings_form[f'p{p}'].data, 
                          settings_form[f'c{p}'].data]
                
                if player[0] not in ['', None, " "]:
                    self.players[p] = player[0]
                    
                self.colors[p] = player[1]
        
        
        # new player    
        if settings_form.xNew.data \
            and settings_form.pNew.data not in ["", None, " "]:
            
            self.players.append(settings_form.pNew.data)
            self.colors.append(settings_form.cNew.data)
            self.n = len(self.players)
        
        return self