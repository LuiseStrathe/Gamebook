
import sys
sys.path.insert(1, "./")
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
@app.route("/rounds/<string:game_id>", methods=["GET", "POST"])
def rounds(game_id):
  
  # verify user
  if verify_session() == False or game_id[0] != 'R': 
    return redirect("/")
    

  # init params
  info = ""
  group_id = session['username']
  group = load_group(group_id)[0]
  result = group.results[group.results.game_id == game_id]
   
  n = result.n_rounds.values[0]
  player_ids = result.info_2.values[0]
  
  
  # game_info: 
    #     0: game_id, 1: title, 2: date, 
    #     3: player_names, 4: player_colors, 
    #     5: comment
  title = result.info_1.values[0]  
  player_names = [group.players[id] for id in player_ids]
  player_colors = [group.colors[id] for id in player_ids]
  date = pd.to_datetime(result.time.values[0]).strftime("%d/%m/%y")
  comment = result.info_3.values[0]
  winner = result.winner_name.values[0]
  game_info = [game_id, title, date, player_names, player_colors, comment]
  
  
  # not finished game
  if winner in ['', None]: 
    
    points = result.result.values[0][0]        
    finished = False
    rounds_form = CloseRoundForm(csrf_enabled=False)
    submit_game_form = SubmitGameForm(csrf_enabled=False)    
    point_entries = [rounds_form[f"pt{str(i)}"]() for i in range(len(player_ids))]   
    
    # input
    if rounds_form.validate_on_submit():

      # get new input points
      new_points = [rounds_form[f"pt{str(i)}"].data for i in range(len(player_ids))]
      new_points = np.array(new_points, dtype=int)
      
      # merge with existing points
      if n == 0: 
        points = np.vstack([new_points, new_points])
      else: 
        # remove & add total row  
        points = np.vstack([points[:-1], new_points])          
        points = np.vstack([points, np.sum(points, axis=0)])   
      
      # update group
      result.loc[0, 'result'] = [points]
      result.loc[0, 'n_rounds'] = n + 1   
      group.results[group.results.game_id == game_id] = result
      group.update_group()
      
      session['round']  = n + 1    
      return redirect(f"/rounds/{game_id}")
    
    else: print("> Submit ROUND - errors", rounds_form.errors)

    
      
    # submit page
    if submit_game_form.validate_on_submit():
      
      if n > 0:
        comment = submit_game_form.comment.data
        end_rounds(group=group, points=points, game_id=game_id, \
          title=title, players=player_ids, comment=comment)
        
        session['round'] = 0
        session['game_id'] = ''
        session['mode'] = ''
        
        return redirect(f"/rounds/{game_id}")
      
      else: 
        print("> Submit GAME - errors", submit_game_form.errors)
        info = "No rounds played yet."
    
  # finished game
  else: 
    finished = True
    points = result.result.values[0]
    rounds_form = ''
    submit_game_form = ''
    point_entries = ''
    
    
  # chart data
  chart_data = create_rounds_chart(points, player_ids)
  
  
  static = 'rounds.html'
  return render_template( 
    static, page=page_html(static, "IN"), info=info,
    rounds_form=rounds_form, point_entries=point_entries, 
    submit_game_form=submit_game_form,
    game_info=game_info, finished=finished, winner=winner,
    round= n + 1, points=points, 
    chart_data=chart_data)
  
  
  
  
# STATS

@app.route("/stats/rounds", methods=["GET", "POST"])
def stats_rounds():
  
  if verify_session() == False and \
    check_key(session['username'], session['key']) == False:
      init_session()
      return redirect(url_for('login', retry=False))  
  
  # init
  group_id = name_to_id(session['username'])
  group = load_group(group_id)[0]
  players = group.players
  logs, winner_chart = gen_rounds_logs(group_id)
  colors = group.colors
  
    
  static = 'stats_rounds.html'  
  return render_template(
    static, page=page_html(static, "IN"),
    players=players, modes=modes, modes_info=modes_info,
    logs=logs, winner_chart=winner_chart, colors=colors,)
  
  