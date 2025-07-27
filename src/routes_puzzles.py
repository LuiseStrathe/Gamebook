
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



###############################################
#                  PUZZLE SITE
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

  choice_logs_delete = \
    [(f"({len(logs) - i}) {logs[i][2]}: \
      {puzzles.title[puzzles.id[0] == logs[i][4]][0].upper()} \
      in {logs[i][6]} ({logs[i][1]})")
      for i in range(len(logs))]
    
  choice_filter = \
    [sorted(set([i[2] for i in logs])),
     sorted(set([i[5] for i in logs])),
     sorted(puzzles.title[puzzles.id == j][0] for j in set([i[4] for i in logs])),
     sorted(set([i[1].partition('/')[2] for i in logs]))]
  
  
  # FORMS
  
  change_puzzle_form = ChangePuzzleForm( \
    puzzles=choice_puzzles, csrf_enabled=False)      

  add_puzzle_form = AddPuzzleForm(csrf_enabled=False) 

  puzzle_record_form = PuzzleRecordForm( \
    players=players, choice_puzzles=choice_puzzles, csrf_enabled=False)    
  
  puzzle_record_delete_form = PuzzleRecordDeleteForm( \
    log_choices=choice_logs_delete, csrf_enabled=False)
  
  puzzle_log_filter_form = PuzzleLogFilterForm(
    players=players, puzzles=choice_puzzles, choice_filter=choice_filter,
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

 
 
  # NEW PUZZLE LOG
  
  if puzzle_record_form.validate_on_submit():
    submit_puzzle_record(id=group_id, form=puzzle_record_form)
    print("> puzzle LOG submitted")
    info = f"{ puzzle_record_form.player.data }'s log was saved."
    return redirect(f"/puzzle")
  
  else:
    print("> Submit LOG - errors: ", puzzle_record_form.errors)
    
    
    
  # DELETE PUZZLE LOG
  
  if puzzle_record_delete_form.validate_on_submit():
    delete_puzzle_log(id=group_id, form=puzzle_record_delete_form, logs=logs)
    print("> puzzle LOG DELETE submitted")
    info = f"{ puzzle_record_delete_form.logs.data }'s log was deleted."
    return redirect(f"/puzzle#puzzleLogs")
  
  else:
    print("> Submit LOG DELETE - errors: ", puzzle_record_delete_form.errors)
  
  
  # FILTER PUZZLE LOGS
  if puzzle_log_filter_form.validate_on_submit():
    print("\n> puzzle LOG FILTER submitted\n")
    return redirect(f"/puzzle#puzzleLogs")
  
  else:
    print("> Submit LOG FILTER - errors: ", puzzle_log_filter_form.errors)
    
    
  static = 'puzzle.html'  
  return render_template(
    static, page=page_html(static, "IN"), 
    add_puzzle_form=add_puzzle_form, 
    change_puzzle_form=change_puzzle_form,
    puzzle_record_form=puzzle_record_form,
    puzzle_record_delete_form=puzzle_record_delete_form,
    puzzle_log_filter_form=puzzle_log_filter_form,
    puzzles=puzzles, colors=player_colors,
    logs=logs, info=info)









###############################################
#               PUZZLE STATS
###############################################

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
  puzzles = pd.DataFrame(group.puzzles, columns=['id', 'title'])
  
  
  # CHARTS
  #   > LABELS =  [0:categories, 1:players (w/ puzzle), 2:colors, 3:puzzles, 4:colors puzzles]
  #   > EXTRA =   [0:#logs player, 1:avg speed player, 2:avg speed puzzle]
  #   > DATA =    [0:#logged, 1:speed player, 2:speed puzzle]
  
  logs = gen_puzzle_logs(group_id)   
  charts = gen_puzzle_charts(logs, puzzles, chart_colors)
  
  #print('\n LABELS:\n', charts[0])
  #print('\n EXTRA:\n', charts[1])
  #print('\n DATA:\n', *charts[2], sep='\n')
     
    
  static = 'stats_puzzle.html'  
  return render_template(
    static, page=page_html(static, "IN"),
    logs=logs, puzzles=puzzles, charts=charts,
    players=players, modes=modes, modes_info=modes_info,)