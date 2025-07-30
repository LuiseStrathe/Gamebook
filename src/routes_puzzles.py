
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
def puzzle_redirect():
  return redirect("/puzzle/all")


@app.route("/puzzle/<string:log_filter_key>", methods=["GET", "POST"])
def puzzle(log_filter_key):  

  
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

  choice_logs_delete = \
    [(f"({len(logs) - i}) {logs[i][2]}: \
      {puzzles.title[puzzles.id[0] == logs[i][4]][0].upper()} \
      in {logs[i][6]} ({logs[i][1]})")
      for i in range(len(logs))]
    
  choice_filter, choice_puzzles = puzzle_choice_filter_gen(logs, puzzles)
    
  filter_data, filtered_logs = puzzle_log_filter_data( \
    log_filter_key, logs, player_colors, puzzles)
  
  if filter_data == 'wrong key':
    return redirect("/puzzle/all#puzzleLogs")
  
  if len(filtered_logs) == 0:
    info = "No logs found for this filter."
  
  
  
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
    
    new_filter_key = puzzle_log_filter_key_gen(puzzle_log_filter_form)
    print(f"\n> puzzle LOG FILTER submitted: {new_filter_key}\n")
    
    if len(new_filter_key) < 7 or len(new_filter_key) > 60 \
      or '__' not in new_filter_key:
        return redirect(f"/puzzle/all#filterDiv")
    else: 
      return redirect(f"/puzzle/{new_filter_key}#filterDiv")
  
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
    logs=filtered_logs, n=len(logs), filter=filter_data, 
    info=info)









###############################################
#               PUZZLE STATS
###############################################


@app.route("/stats/puzzle")
def stats_redirect():
  return redirect("/stats/puzzle_all")


@app.route("/stats/puzzle_<string:log_filter_key>", methods=["GET", "POST"])
def stats_puzzle_all(log_filter_key):
  
  if verify_session() == False and \
    check_key(session['username'], session['key']) == False:
      init_session()
      return redirect(url_for('login', retry=False))  

  
  
  # INIT
  
  group_id = name_to_id(session['username'])
  group = load_group(group_id)[0]
  players = group.players
  puzzles = pd.DataFrame(group.puzzles)
  player_colors = {}
  for p in range(group.n):
    player_colors[players[p]] = group.colors[p]

  
  # LOGS & FILTERS
  
  logs = gen_puzzle_logs(group_id)
  
  filter_data, filtered_logs = puzzle_log_filter_data( \
    log_filter_key, logs, player_colors, puzzles)
  
  choice_filter, choice_puzzles = puzzle_choice_filter_gen(logs, puzzles)
  puzzle_log_filter_form = PuzzleLogFilterForm(
    players=players, puzzles=choice_puzzles, choice_filter=choice_filter,
    csrf_enabled=False)   
  
  if puzzle_log_filter_form.validate_on_submit():
    
    new_filter_key = puzzle_log_filter_key_gen(puzzle_log_filter_form)
    print(f"\n> puzzle LOG FILTER submitted: {new_filter_key}\n")
    
    if len(new_filter_key) < 7 or len(new_filter_key) > 60 \
      or '__' not in new_filter_key:
        return redirect(f"/stats/puzzle_all#filterDiv")
    else: 
      return redirect(f"/stats/puzzle_{new_filter_key}#filterDiv")  

  
  # CHARTS
  
  #   > LABELS =  [0:categories, 1:players (w/ puzzle), 2:colors, 3:puzzles, 4:colors puzzles]
  #   > EXTRA =   [0:#logs player, 1:avg speed player, 2:avg speed puzzle]
  #   > DATA =    [ chart 0:#logged [player, category], 
  #                 chart 1:speed player, 
  #                 chart 2:speed puzzle]  
  
  charts = gen_puzzle_charts(logs, puzzles, chart_colors)
  
  #print('\n LABELS:\n', charts[0])
  #print('\n EXTRA:\n', charts[1])
  #print('\n DATA:\n', *charts[2], sep='\n')
     
    
  static = 'stats_puzzle.html'  
  
  return render_template(
    static, page=page_html(static, "IN"),
    puzzles=puzzles, players=players, colors=player_colors,
    n=len(logs), logs=filtered_logs, 
    charts=charts,
    puzzle_log_filter_form=puzzle_log_filter_form, filter=filter_data, 
    modes=modes, modes_info=modes_info)