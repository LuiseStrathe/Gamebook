
import os
import sys
sys.path.insert(1, "./")

import pickle
import numpy as np
import pandas as pd
from flask import session

from src.my_params import *


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

    def __init__(self, name, key, players, motto=None):

        self.name = name
        self.id = name_to_id_create(name)
        self.players = players
        self.player_info = pd.DataFrame(columns=player_cols)
        self.n = len(players)
        self.key = key
        self.results = pd.DataFrame(columns=result_cols)
        self.motto = motto
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

    def update_group(self):
        with open(self.filepath, "wb") as f:
            pickle.dump(self, f)

