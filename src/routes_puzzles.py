
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



###############################################
#                     PUZZLE 
###############################################


@app.route("/puzzle", methods=["GET", "POST"])
def puzzle():  
  
  
  # INIT
  
  if session['status'] != 'IN':
    return redirect("/")
  
  info=''
  group_id = name_to_id(session['username'])
  group = load_group(group_id)[0]
  
  players = group.players
  puzzles = pd.DataFrame(group.puzzles)
  logs = gen_puzzle_logs(group_id)
  
  player_colors = {}
  for p in range(group.n):
    player_colors[players[p]] = group.colors[p]
       
  choice_puzzles = \
    [(f"{puzzles.id.iloc[i]}: {puzzles.title.iloc[i]} ({puzzles.pcs.iloc[i]} pcs.)")
    for i in range(len(puzzles))]
  
  
  change_puzzle_form = ChangePuzzleForm( \
    puzzles=choice_puzzles, csrf_enabled=False)      

  add_puzzle_form = AddPuzzleForm(csrf_enabled=False) 

  puzzle_record_form = PuzzleRecordForm( \
    players=players, choice_puzzles=choice_puzzles,
    csrf_enabled=False)    
  
     
  
  # ADD PUZZLE  

  if add_puzzle_form.validate_on_submit():
    info = add_puzzle(group_id=group_id, add_puzzle_form=add_puzzle_form)
    if info != "":
      print("> puzzle ADD submitted")
    else: return redirect(f"/puzzle#puzzleLib")
  
  else:
    print("> Submit ADD - errors", add_puzzle_form.errors)
 
  
  # CHANGE PUZZLE 

  if change_puzzle_form.validate_on_submit():
    print("> puzzle CHANGE submitted")
    change_puzzle(id=group_id, form=change_puzzle_form)
    
    info=f"Puzzle {change_puzzle_form.puzzle_change.data} changed."
    return redirect(f"/puzzle#puzzleLib")
  
  else:
    print("> Submit CHANGE - errors:", change_puzzle_form.errors)

 
  # LOGS
  
  if puzzle_record_form.validate_on_submit():
    submit_puzzle_record(id=group_id, form=puzzle_record_form)
    print("> puzzle LOG submitted")
    
    info = f"{ puzzle_record_form.player.data }'s Log was saved."
    return redirect(f"/puzzle")
  
  else:
    print("> Submit LOG - errors: ", puzzle_record_form.errors)
    
    
  static = 'puzzle.html'  
  return render_template(
    static, page=page_html(static, "IN"), 
    add_puzzle_form=add_puzzle_form, 
    change_puzzle_form=change_puzzle_form,
    puzzle_record_form=puzzle_record_form,
    puzzles=puzzles, colors=player_colors,
    logs=logs, info=info)




@app.route("/stats/puzzle", methods=["GET", "POST"])
def stats_puzzle():
  
  if verify_session() == False and \
    check_key(session['username'], session['key']) == False:
      init_session()
      return redirect(url_for('login', retry=False))  
  
  # init
  group_id = name_to_id(session['username'])
  group = load_group(group_id)[0]
  players = group.players
  logs = gen_puzzle_logs(group_id)
  
    
  static = 'stats_puzzle.html'  
  return render_template(
    static, page=page_html(static, "IN"),
    players=players, logs=logs, 
    modes=modes, modes_info=modes_info,)