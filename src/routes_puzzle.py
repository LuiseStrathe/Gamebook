
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



# LIST of all puzzles
@app.route("/puzzle/<string:group_id>/0", methods=["GET", "POST"])
def puzzle_list(group_id):  
  
  # verify user
  if session['status'] != 'IN':
    return redirect("/")

  # init params
  group = load_group(group_id)    
  add_puzzle_form =   AddPuzzleForm(csrf_enabled=False)  
  
  # add puzzle
  if add_puzzle_form.validate_on_submit():
    add_puzzle(group_id=group_id, add_puzzle_form = add_puzzle_form)
    return redirect(f"/puzzle/{group_id}/0")
  
    
  return render_template("puzzle_list.html",
                            add_puzzle_form=add_puzzle_form, 
                            group=group, puzzles=pd.DataFrame(group.puzzles))




# NEW RECORD
@app.route("/puzzle/<string:group_id>/<int:puzzle_id>", methods=["GET", "POST"])
def puzzle_record(group_id, puzzle_id):  
  
  # verify user
  if session['status'] != 'IN':
    return redirect("/")
  print(f"Puzzle id {puzzle_id} of group {group_id} opened.")


  # init params
  group = load_group(group_id)    
  
  class PuzzleRecordForm(FlaskForm):
    player = SelectMultipleField("Player", choices=group.players, validators=[DataRequired()])
    hours = IntegerField("Hours", default=0)
    minutes = IntegerField("Minutes", default=0, validators=[DataRequired()])
    seconds = IntegerField("Seconds", default=0)
    comment = TextAreaField("Comment (optional)")
    submit = SubmitField("Enter your Puzzle Record to the GameBook")
  puzzle_record_form =   PuzzleRecordForm(csrf_enabled=False)  
  
  
  if puzzle_record_form.validate_on_submit():
    submit_puzzle_record(group_id=group_id, puzzle_id=puzzle_id,
                         puzzle_record_form=puzzle_record_form)
    return redirect(f"/puzzle/{group_id}/0")
  
  return render_template("puzzle_record.html", 
                          puzzle_record_form=puzzle_record_form,
                          group=group)
  


# STATS
@app.route("/<string:group_id>/puzzles")
def puzzle_stats(group_id):
  
  if session['status'] == 'OUT':
    return redirect('/')
  
  group = load_group(group_id)
  records = group.results[group.results['g_mode'] == 'puzzle']
  
  return render_template("puzzle_stats.html",
                         group=group, records=records)