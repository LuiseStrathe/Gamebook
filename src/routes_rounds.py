
import sys
sys.path.insert(1, "./")
from app import app

from src.my_forms import *
from src.my_params import *
from src.my_classes import *
from src.my_fun import *
from src.routes import *
from src.routes_groups import *

from flask import Flask, render_template, request, url_for, redirect, flash, session
import numpy as np
import pandas as pd
from datetime import datetime



# PLAY
@app.route("/rounds/<string:group_id>/<string:game_id>/<int:round>", methods=["GET", "POST"])
def rounds(group_id, game_id, round):
  
  # init
  base =              get_base()
  if session['status'] != 'IN':
                      redirect_link = f"/rounds/random/{game_id}/{round}"
  else:               redirect_link = '/'
  
  
  # verify user
  if round != session['round']:
    return redirect(f"/rounds/{group_id}/{game_id}/{session['round']}")
  if group_id != session['username']:
    if group_id == 'random': pass
    else: return redirect(f"{redirect_link}")
  print(f"Round {round} of game {game_id} of group {group_id} started")


  # init params
  n =                 int(session['num_players'])
  rounds_form =       CloseRoundForm(csrf_enabled=False)
  submit_game_form =  SubmitGameForm(csrf_enabled=False)
  clear_game_form =   ClearGameForm(csrf_enabled=False)    
  if group_id == 'random': 
                      group = create_random_group()
  else:               group = load_group(group_id)
  
  
  # generate table
  if round == 0:      
                      start = True
                      points = np.zeros((2,n))
  else:               
                      start = False
                      points = np.load(f"{path_data}tmp/rounds/{game_id}.npy") 
                      
  template_entries =  [rounds_form.pt1(), rounds_form.pt2(), rounds_form.pt3(), rounds_form.pt4(), 
                      rounds_form.pt5(), rounds_form.pt6(), rounds_form.pt7(), rounds_form.pt8()]   
  point_entries =     [e for e in template_entries[:n]]
  
  print('Now enter your points')
  
  
  # input
  if rounds_form.validate_on_submit():
    print(f"Round {session['round']} sumbitted")

    template_data =   [rounds_form.pt1.data, rounds_form.pt2.data, rounds_form.pt3.data, rounds_form.pt4.data, 
                      rounds_form.pt5.data, rounds_form.pt6.data, rounds_form.pt7.data, rounds_form.pt8.data]
    new_points = np.array([template_data[:n]])
    print('Entered Points:', new_points)
    
    if round == 0:    points = new_points
    else:             points = np.vstack([points, new_points])  
               
    points =          np.vstack([points, np.sum(points, axis=0)])
    np.save(f"{path_data}tmp/rounds/{game_id}", points)  
    
    print('Points:\n”',points.shape)
    print(points)
    
    session['round']  += 1    
    return redirect(f"/rounds/{group_id}/{game_id}/{session['round']}")
  

  # exit game
  if clear_game_form.validate_on_submit():
    print(f"Game {game_id} is now cleared")
    session['game_id'] = ''
    if redirect_link == '/': return redirect('/')
    else: return redirect(f"/gamebook")
    
  # submit page
  if submit_game_form.validate_on_submit():
    print(f"Game {game_id} submitted")
    end_rounds(group, points, game_id=game_id, info=submit_game_form.info.data)
    return redirect(f"{redirect_link}")
  
  
  return render_template("rounds.html",
                            modes=modes, descriptions=descriptions, base=base,
                            rounds_form=rounds_form, submit_game_form=submit_game_form, clear_game_form=clear_game_form, 
                            group=group, game_id=game_id, n=n, start=start,  
                            round=round, points=points[:-1],
                            point_entries=point_entries)


# PAGE
@app.route("/<string:group_id>/rounds/<string:game_id>")
def rounds_page(group_id, game_id):
  
  if session['status'] != 'OUT':
    return redirect('/')
  
  group = load_group(group_id)
  result = group.results['game_id' == game_id]
  time = result['time'].strftime("%d.%m.%Y %H")
  points = np.load(f"{path_data}rounds/{game_id}.npy")
  
  return render_template("rounds_page.html",
                         group=group, game_id=game_id, time=time)