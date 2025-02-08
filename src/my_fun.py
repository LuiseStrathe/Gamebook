

''' Functions for group data and session management '''



import os
import sys
sys.path.insert(1, "./")

import pickle
import numpy as np
import pandas as pd
from flask import session

from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *




###############################################
#                     SYSTEM 
###############################################


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
    
    elif force_in_out == 'IN':
        page_html[0] = "__head_in.html"
        
    else:
        page_html[0] = "__head_out.html"
        
    return page_html



###############################################
#                     GROUP 
###############################################



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
        check = f'{id}.pkl' not in os.listdir(f'{path_data}groups/')
        
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


