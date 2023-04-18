
import sys
sys.path.insert(1, "./")
from app import app

from src.my_forms import *
from src.my_params import *
from src.my_classes import *
from src.my_fun import *
from src.routes_rounds import *
from src.routes import *

from flask import Flask, render_template, request, url_for, redirect, flash, session
from os.path import exists



#### GROUP MAINS ####

# Group page
@app.route("/group/<string:group_id>", methods=["GET", "POST"])
def group(group_id):
  
  if check_key(session['username'], session['key']):
    group = load_group(group_id)
    return render_template("group.html", 
                           descriptions=descriptions, modes=modes, 
                           group=group)
    
  else: return redirect('login')


# enter GameBook
@app.route("/gamebook")
def enter_gamebook():
  if check_key(session['username'], session['key']):    
    return redirect(f"/gamebook/{session['username']}")
  else: return redirect('login')

# GameBook
@app.route("/gamebook/<string:group_id>", methods=["GET", "POST"])
def gamebook(group_id):
  
  if check_key(session['username'], session['key']):
    group = load_group(group_id)
    return render_template("gamebook.html", 
                           descriptions=descriptions, modes=modes, 
                           group=group)
    
  else: return redirect('login')
  
  
# Random 
@app.route("/random_group", methods=["GET", "POST"])
def random_group():
  random_form = RandomGroup(csrf_enabled=False)
  
  if random_form.validate_on_submit():
    players = [random_form.p1.data, random_form.p2.data, \
                      random_form.p3.data, random_form.p4.data]
    players = [p for p in players if p != '']
    session['group_id'] = 'random'
    session['num_players'] = len(players)
    session['status'] = 'OUT'
    session['random_players'] = players
    return redirect(f"/start/rounds/random")

  return render_template("random.html",
                         modes=modes, descriptions=descriptions,
                         random_form=random_form)
  
  
# Start game
@app.route("/start/<string:mode>/<string:group_id>",  methods=["GET", "POST"])
def game_start(group_id, mode):
  
  game_id =             gen_game_id(mode)
  session['round'] =    0
  session['game_id'] =  game_id
  check =               check_key(session['username'], session['key']) and (session['status'] == 'IN')
  
  if group_id=='random' or check:
    return redirect(f"/{mode}/{group_id}/{game_id}/0")
  
  return redirect('/')



#### ADMIN ####

# Login
@app.route('/login', methods = ['GET', 'POST'])
def login():
  
  if 'retry' in request.args:
    retry = request.args['retry']
  else: retry = False
  
  if request.method == 'POST':
      name, key = request.form['username'], request.form['key']
      id = name_to_id(name)
      if exists(f'{path_data}groups/{id}.pkl'):
        if check_key(id, key):
          session['username'] = id
          session['key'] = key
          session['status'] = 'IN'
          session['num_players'] = load_group(id).n
          session['round'] = 0
          session['game_id'] = 0
          print(name, 'now logged in')
          return redirect(f"/group/{id}")
      else: 
        init_session()
        retry = True
        return redirect(url_for('login', retry=retry))
      
  return render_template('group_login.html', retry=retry)


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
      group = My_Group(name=group_form.name.data, motto=group_form.motto.data,
                    key=group_form.key.data, players=players)
      print(f'New group created: \n{group.name}({group.id})\n{players}')
      session['username'] = group.id
      session['key'] = group.key
      session['num_players'] = group.n
      session['status'] = 'IN'
      print(group.name, 'now logged in')
      return redirect(f"/group/{group.id}")
    
    else: print("ERROR: group probably arleady exists")
    
  return render_template("group_create.html", 
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
  
  return render_template("group_delete.html", 
                         group_name=group_name, delete_form=delete_form)


