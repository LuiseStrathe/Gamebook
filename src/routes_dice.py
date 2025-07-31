
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


###############################################
#               DICE PLAY
###############################################


@app.route("/dice/<string:game_id>", methods=["GET", "POST"])
def dice(game_id):
    
  # VERIFY
  if verify_session() == False or game_id[0] != 'D': 
    return redirect("/")
  
  group_id = session['username']
  group = load_group(group_id)[0]
    
  if game_id not in group.results.game_id.values:
    return redirect("/")
  
  
  # INIT
  info = ""

  result = group.results[group.results.game_id == game_id]
  game_data = result.g_data.values[0]
  n = result.n_rounds.values[0]
  player_ids = result.player_ids.values[0]
  player_names = [group.players[id] for id in player_ids]
  player_colors = [group.colors[id] for id in player_ids]
  date = pd.to_datetime(result.time_stamp.values[0]).strftime("%d/%m/%y")
  comment = result.comment.values[0]
  winners = winner_str(group.players, result.winner_id.values[0])

  
  dice_form = PlayDiceForm(csrf_enabled=False)
  submit_game_form = None  
  
  # STATUS
  if n < 13: status = 'play'
  elif n == 13: status = 'final'
  else: status = 'done'
  
    
  # PLAYING
  if status == 'play': 
    
    # submit a round
    if dice_form.validate_on_submit():
      info = next_dice(group, game_id, game_data, dice_form)
      
      if info == '':      
        return redirect(f"/dice/{game_id}")

    else: print("> Submit DICE - errors:", dice_form.errors)
    
  
  elif status == 'final':
    submit_game_form = SubmitGameForm(csrf_enabled=False)
    
    # submit game
    if submit_game_form.validate_on_submit():
      comment = submit_game_form.comment.data
      winner_ids = result.winner_id.values[0]
      end_dice(group, game_id, player_ids, game_data, winner_ids, comment)
      
      return redirect(f"/group/{group_id}")
      
    else: print("> Submit GAME - errors:", submit_game_form.errors)
    
  
  # DATA
  game_info = [status, game_id, date,       # 0-2 (game)
              player_names, player_colors,  # 3-4 (players)
              comment, winners,             # 5-6 (final)
              dice_rows[1], dice_rows[2]]   # 7   (labels)

  point_entries = create_dice_point_entries(
    game_data, n, dice_form, len(player_ids))
  
  chart_data = create_dice_game_chart(game_data=game_data, n=int(n))
               
  static = "dice.html"
  return render_template(
    static, page=page_html(static, "IN"), info=info,
    game_info=game_info, round=int(n),
    dice_form=dice_form, submit_game_form=submit_game_form,
    point_entries=point_entries, chart_data=chart_data,)





###############################################
#               DICE STATS
###############################################


@app.route("/stats/dice")
def stats_dice_redirect():
  return redirect("/stats/dice_all")



@app.route("/stats/dice_<string:log_filter_key>", methods=["GET", "POST"])
def stats_dice(log_filter_key):
  
  if verify_session() == False and \
    check_key(session['username'], session['key']) == False:
      init_session()
      return redirect(url_for('login', retry=False))  
  
  
  # INIT
  
  group_id = name_to_id(session['username'])
  group = load_group(group_id)[0]
  players = group.players
  logs, winner_chart = gen_dice_stats(group_id)
  player_colors = {}
  for p in range(group.n):
    player_colors[players[p]] = group.colors[p]
    

  # LOGS & FILTERS
  
  logs, winner_chart = gen_dice_stats(group_id)
  choice_filter = dice_choice_filter_gen(logs, players)
  filter_data, filtered_logs = dice_log_filter_data(log_filter_key, logs, player_colors)
  
  
  log_filter_form = DiceLogFilterForm(
    choice_filter=choice_filter, csrf_enabled=False)   
  
  if log_filter_form.validate_on_submit():
    
    new_filter_key = dice_log_filter_key_gen(log_filter_form)
    print(f"\n> dice LOG FILTER submitted: {new_filter_key}\n")
    
    if len(new_filter_key) < 7 or len(new_filter_key) > 60 \
      or '__' not in new_filter_key:
        return redirect(f"/stats/dice_all#filterDiv")
    else: 
      return redirect(f"/stats/dice_{new_filter_key}#filterDiv")  
    
    
  static = 'stats_dice.html'  
  return render_template(
    static, page=page_html(static, "IN"),
    players=players, modes=modes, modes_info=modes_info,
    logs=filtered_logs, n = len(logs), filter= filter_data,
    log_filter_form=log_filter_form, 
    winner_chart=winner_chart, colors=player_colors,)


