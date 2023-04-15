
import sys
sys.path.insert(1, "./")
from app import app
from src.helper import *
from src.forms import *
from src.my_params import *

from flask import Flask, render_template, request, url_for, redirect, flash, session



#### INDEX ####

# HOME
@app.route("/")
def index():
  
  if ('username' in session) and \
      check_key(session['username'], session['key']):
      session['status'] = 'IN'
      return redirect('group/' + session['username'])
  else: init_session()
  
  return render_template("index.html", 
                         modes=modes, descriptions=descriptions, about_info=about_info)



#### GROUP ####

# Group
@app.route("/group/<string:group_id>", methods=["GET", "POST"])
def group(group_id):
  
  if check_key(session['username'], session['key']):
    group = load_group(group_id)
    session['num_players'] = group.n
    return render_template("group.html", 
                           descriptions=descriptions, modes=modes, group=group)
    
  else: return redirect('login')
  
# Random 
@app.route("/random_group", methods=["GET", "POST"])
def random_group():
  session['num_players'] = 3
  return render_template("random.html",
                         modes=modes, descriptions=descriptions)



#### ADMIN ####

# Login
@app.route('/login', methods = ['GET', 'POST'])
def login():
  
  if request.method == 'POST':
      name, key = request.form['username'], request.form['key']
      id = name_to_id(name)
      if check_key(id, key):
        session['username'] = id
        session['key'] = key
        session['status'] = 'IN'
        print(name, 'now logged in')
        return redirect(f"/group/{id}")
      else: 
        init_session()
        return render_template('400.html')
      
  return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
   init_session()
   return redirect(url_for('index'))


# Register
@app.route("/create_group", methods=["GET", "POST"])
def create_group():
  group_form = GroupForm(csrf_enabled=False)
  
  if group_form.validate_on_submit():  
    name = group_form.name.data
    key = group_form.key.data
    check, id = check_name(name)  
    
    if check:
      players = create_players(group_form)
      group = Group(name=group_form.name.data, motto=group_form.motto.data,
                    key=group_form.key.data, players=players)
      print(f'New group created: \n{group.name}({group.id})\n{players}')
      session['username'] = group.id
      session['key'] = group.key
      session['num_players'] = group.n
      session['status'] = 'IN'
      print(group.name, 'now logged in')
      return redirect(f"/group/{group.id}")
    
    else: print("ERROR: group probably arleady exists")
    
  return render_template("create_group.html", 
                         group_form=group_form)

# Delete
@app.route('/delete/<string:group_id>', methods=["GET", "POST"])
def delete(group_id):
  delete_form = DeleteForm(csrf_enabled=False)
  group_name = id_to_name(group_id)
  
  if delete_form.validate_on_submit():
    if check_key(group_id, delete_form.key.data):
        init_session()
        delete_group(group_id)
        return redirect('/')
  
  return render_template("delete.html", 
                         group_name=group_name, delete_form=delete_form)



#### MODES ####


# Rounds
@app.route("/rounds/<string:group_id>", methods=["GET", "POST"])
def rounds(group_id):
  
  rounds_form = CloseRoundForm(csrf_enabled=False)
  submit_game_form = SubmitGameForm(csrf_enabled=False)
  clear_game_form = ClearGameForm(csrf_enabled=False)
  
  game_id = gen_game_id()
  session['game_id'] = game_id
  check = check_key(session['username'], session['key']) and (session['status'] == 'IN')
  
  if group_id=='random' or check:
    if group_id=='random': 
      group = create_random_group(n)
    else: 
      group = load_group(group_id)
    return render_template("rounds.html",
                            modes=modes, descriptions=descriptions, 
                            group=group, game_id=game_id, rounds_form=rounds_form,
                            submit_game_form=submit_game_form, clear_game_form=clear_game_form, 
                            n=session['num_players'])
  return redirect('/')



#### GENERAL ####

# about
@app.route("/about")
def about():
  base = 'base.html'
  if session['status'] == 'IN':
    base = 'base_in.html'
  return render_template("about.html", base=base,
                         about_info=about_info)


# errors
@app.errorhandler(400) 
def not_found(e): 
  return render_template("400.html") 

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

@app.errorhandler(500) 
def not_found(e): 
  return render_template("404.html") 