
import sys
sys.path.insert(1, "./")
from Gamebook.gamebook_app import app

from Gamebook.src.my_forms import *
from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *
from Gamebook.src.my_fun import *
from Gamebook.src.routes import *
from Gamebook.src.routes_groups import *

from flask import Flask, render_template, request, url_for, redirect, flash, session
import numpy as np
import pandas as pd
from datetime import datetime



# PLAY
@app.route("/rounds/<string:game_id>", methods=["GET", "POST"])
def rounds(game_id):
  
  # verify user
  if verify_session() == False: 
    if session['username'] == 'random': pass
    else: return redirect("/")
    

  # init params
  info = ""
  group_id = session['username']
  group = load_group(group_id)[0]
  result = group.results[group.results.game_id == game_id]
   
  n = result.n_rounds.values[0]
  player_ids = result.info_2.values[0]
  points = result.result.values[0]
  
  # game_info: 
    #     0: game_id, 1: title, 2: date, 
    #     3: player_names, 4: player_colors, 
    #     5: comment
  title = result.info_1.values[0]  
  player_names = [group.players[id] for id in player_ids]
  player_colors = [group.colors[id] for id in player_ids]
  date = pd.to_datetime(result.time.values[0]).strftime("%d/%m/%y")
  comment = result.info_3.values[0]
  game_info = [game_id, title, date, player_names, player_colors, comment]
  
  
  # not finished game
  if result.winner_name.values[0] == '': 
    
    finished = False
    rounds_form = CloseRoundForm(csrf_enabled=False)
    submit_game_form = SubmitGameForm(csrf_enabled=False)    
    template_entries = [rounds_form[f"pt{str(i)}"]() for i in range(len(player_ids))]   
    point_entries = [rounds_form[f"pt{str(i)}"].data for i in range(len(player_ids))]
    commennt = ''    
    
    # input
    if rounds_form.validate_on_submit():

      template_data =   [rounds_form.pt1.data, rounds_form.pt2.data, rounds_form.pt3.data, rounds_form.pt4.data, 
                        rounds_form.pt5.data, rounds_form.pt6.data, rounds_form.pt7.data, rounds_form.pt8.data]
      new_points = np.array([template_data[:n]])
      
      if n == 0: points = new_points
      else: points = np.vstack([points[:-1], new_points])  
                
      points = np.vstack([points, np.sum(points, axis=0)])
      group.result.loc[group.result.game_id == game_id, 'points'] = points
      group.result.loc[group.result.game_id == game_id, 'n_rounds'] = n + 1 
      
      session['round']  = n + 1    
      return redirect(f"/rounds/{game_id}")
    
      
    # submit page
    if submit_game_form.validate_on_submit():
      
      # info_3: user note
      comment = submit_game_form.r_comment.data
      end_rounds(group=group, points=points, game_id=game_id, \
        title=title, players=player_ids, comment=comment)
      
      return redirect(f"/rounds/{game_id}")
    
  
  else: finished = True
  
  static = 'rounds.html'
  return render_template( 
    static, page=page_html(static, "IN"), info=info,
    rounds_form=rounds_form, point_entries=point_entries, 
    submit_game_form=submit_game_form,
    game_info=game_info, finished=finished,  
    round= n + 1, points=points)