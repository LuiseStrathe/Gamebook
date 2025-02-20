
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
  
  # VERIFY
  if verify_session() == False or game_id[0] != 'R': 
    return redirect("/")


  # INIT
  info = ""
  group_id = session['username']
  group = load_group(group_id)[0]
  result = group.results[group.results.game_id == game_id].copy()
  points = np.array(result.g_data.values[0], dtype=int)
  n = result.n_rounds.values[0]
  player_ids = result.player_ids.values[0]
  point_entries = []
  
    
  title = result.title.values[0]  
  player_names = [group.players[id] for id in player_ids]
  player_colors = [group.colors[id] for id in player_ids]
  date = pd.to_datetime(result.time_stamp.values[0]).strftime("%d/%m/%y")
  comment = result.comment.values[0]
  winners = winner_str(group.players, result.winner_id.values[0])
  
  
  rounds_form = None
  submit_game_form = None
  

  # STATUS
  if winners in ['', None]: status = 'play'
  else: 
    status = 'done'
  
  # PLAYING
  if status == 'play': 

    rounds_form = CloseRoundForm(csrf_enabled=False)
    submit_game_form = SubmitGameForm(csrf_enabled=False)    
    point_entries = [rounds_form[f"pt{str(i)}"]() for i in range(len(player_ids))]   
    
    # submit round
    if rounds_form.validate_on_submit():

      info = next_rounds(
        group, game_id, result, points, n, rounds_form, len(player_ids))
      
      if info == '':
        return redirect(f"/rounds/{game_id}")
    
    else: print("> Submit ROUND - errors", rounds_form.errors)

      
    # submit game
    if submit_game_form.validate_on_submit():
      
      if n > 0:
        comment = submit_game_form.comment.data
        end_rounds(group=group, points=points, game_id=game_id, \
          title=title, players=player_ids, comment=comment)
        
        return redirect(f"/rounds/{game_id}")
      
      else: 
        print("> Submit GAME - errors", submit_game_form.errors)
        info = "No rounds played yet."
    
    
  # DATA
  game_info = [game_id, title, date, player_names, player_colors, comment]
  chart_data = create_rounds_chart(points, player_ids)
  
  static = 'rounds.html'
  return render_template( 
    static, page=page_html(static, "IN"), info=info,
    rounds_form=rounds_form, point_entries=point_entries, 
    submit_game_form=submit_game_form,
    game_info=game_info, status=status, winners=winners,
    round= n + 1, points=points, chart_data=chart_data)
  
  
  
  
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
  logs, winner_chart = gen_rounds_stats(group_id)
  colors = group.colors
  
    
  static = 'stats_rounds.html'  
  return render_template(
    static, page=page_html(static, "IN"),
    players=players, modes=modes, modes_info=modes_info,
    logs=logs, winner_chart=winner_chart, colors=colors,)
  
  