
import sys
sys.path.append("./")
from Gamebook.gamebook_app import app

from Gamebook.src.my_forms import *
from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *
from Gamebook.src.my_fun_games import *
from Gamebook.src.routes import *
from Gamebook.src.routes_groups import *

from flask import Flask, render_template, request, url_for, redirect, flash, session
import numpy as np
import pandas as pd
from datetime import datetime



# PLAY
@app.route("/dice/<string:game_id>", methods=["GET", "POST"])
def dice(game_id):
    
  # verify
  if verify_session() == False or game_id[0] != 'D': 
    return redirect("/")
  
  
  
  # init params
  info = ""
  group_id = session['username']
  group = load_group(group_id)[0]
  result = group.results[group.results.game_id == game_id]


  # game_info: 
    #     0: game_id, 1: title, 2: date, 
    #     3: player_names, 4: player_colors, 
    #     5: comment
    
               
  static = "dice.html"
  return render_template(
    static, page=page_html(static, "in"), info=info,)




# STATS
@app.route("/stats/dice", methods=["GET", "POST"])
def stats_dice():
  
  if verify_session() == False and \
    check_key(session['username'], session['key']) == False:
      init_session()
      return redirect(url_for('login', retry=False))  
  
    
  static = 'stats_dice.html'  
  return render_template(
    static, page=page_html(static, "IN"),
    modes=modes, modes_info=modes_info,)


