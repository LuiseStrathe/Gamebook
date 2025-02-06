
import sys
sys.path.append("./")
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


# START
@app.route("/dice/<string:group_id>/<string:game_id>/start", \
           methods=["GET", "POST"])
def dice_start(group_id, game_id):
  
  # init
  if session['status'] != 'IN' or group_id != session['username']:
      redirect('/')
  group =             load_group(group_id)
  
  class DiceStartForm(FlaskForm):
    players = SelectMultipleField("Players", 
                                  choices=[p for p in group.players])
    sums = BooleanField("Show Sums", default=False)
    submit = SubmitField("Start Dice Game")
  start_form =       DiceStartForm(csrf_enabled=False)

  if start_form.validate_on_submit():

    players =   start_form.players.data
    session['players'] = players
    session['round']  = 1    
    points = np.full((13, len(players)), np.nan)
    np.save(f"{path_data}tmp/dice/{game_id}.npy", points)
    
    return redirect(f"/dice/{group_id}/{game_id}/1")
  
  static = "dice_start.html"
  return render_template(static, page=page_html(static, "in"), 
                            group=group, game_id=game_id,
                            start_form=start_form)


# PLAY
@app.route("/dice/<string:group_id>/<string:game_id>/<int:round>", 
           methods=["GET", "POST"])
def dice(group_id, game_id, round):
  
  # init
  if session['status'] != 'IN' or group_id != session['username']:
      redirect('/')
  if round != session['round']:
    return redirect(f"/dice/{group_id}/{game_id}/{session['round']}")
  
  print(f">> DICE ({round}/13, {game_id}) of {group_id}")
  points = np.load(f"{path_data}tmp/dice/{game_id}.npy")
  group =   load_group(group_id)
  players = session['players']
  n =       len(players)
  n_fields = n * (14 - round)
  input_error = ''
  
  # form
  class DiceForm(FlaskForm):
    for i in range(n_fields):
      exec(f"field_{i} = IntegerField('', default=np.nan)")
    submit = SubmitField("Close this Round")  
  dice_form =       DiceForm(csrf_enabled=False)
  
  # chart
  chart = points.copy().tolist()
  counter = 0
  for r in range(13):
    for p in range(n):
      if np.isnan(chart[r][p]):
        exec(f"chart[r][p] = dice_form.field_{counter}()")
        counter += 1
  
  
  # next round
  if dice_form.submit.data:
    print('Submit clicked.')
    
    inputs = []
    for i in range(n_fields):
      exec(f"inputs.append(dice_form.field_{i}.data)")
    points = dice_update_points(points, inputs)
     
    check, checks = check_dice_points(points, round + 1)
    if ~check:
      print('Check failed.')
      input_error = 'Please check your inputs.'
    
    else:
      np.save(f"{path_data}tmp/dice/{game_id}.npy", points)
      
      
      if session['round'] == 13:
        group.update_group(group_id, game_id, points, 'dice')
        return redirect(f"/{group_id}/dice/{game_id}")
      
      else:
        session['round']  += 1
        return redirect(f"/dice/{group_id}/{game_id}/{session['round']}")
               
  static = "dice.html"
  return render_template(static, page=page_html(static, "in"), 
                          input_error=input_error,
                          dice_form=dice_form, dice_rows=dice_rows,
                          group=group, game_id=game_id, n=n, 
                          round=round, chart=chart, players=players)




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


