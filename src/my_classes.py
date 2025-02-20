
import os
import sys
sys.path.append("./")

import pickle
import numpy as np
import pandas as pd
from flask import session

from Gamebook.src.my_params import *
from Gamebook.src.my_fun import *




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


# duplicate from my_fun.py
def encrypt_key(key):
    
    path = f'{path_data}/server/salt.txt'
    with open(path, "rt") as f:
        salt = str(f.readline())
    
    hash = 65
    salted = key + salt
    for ch in salted:
        hashed = ( hash*281  ^ ord(ch)*987) & 0xFFFFFFFF
    
    return str(hashed)



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
        self.slogan = slogan       
        
        self.results = pd.DataFrame(columns=result_cols)
        self.puzzles = pd.DataFrame(columns=puzzle_cols)
                
        self.key = encrypt_key(key)        
        self.filepath = f'{path_data}groups/{self.id}.pkl'

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
                        
        
        for p in range(self.n):           
            
            # existing player
            if settings_form[f'x{p}'].data:
                
                player = [settings_form[f'p{p}'].data, 
                          settings_form[f'c{p}'].data]
                
                if player[0] not in ['', None, " "]:
                    
                    if player[0] in self.players:
                        return False
                    
                    else:
                        self.players[p] = player[0]
                
                self.colors[p] = player[1]
        
        
        # new player    
        if settings_form.xNew.data \
            and settings_form.pNew.data not in ["", None, " "]:
            
            new_player = [settings_form.pNew.data, 
                          settings_form.cNew.data]
            
            if new_player[0] not in self.players:
                self.players.append(new_player[0])
                self.colors.append(new_player[1])
                self.n = len(self.players)
                
            else:
                return False
        
        return self