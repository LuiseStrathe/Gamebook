
import sys
sys.path.insert(1, "./")
from Gamebook.gamebook_app import app

from Gamebook.src.my_forms import *
from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *
from Gamebook.src.my_fun import *
from Gamebook.src.routes import *
from Gamebook.src.routes_rounds import *
from Gamebook.src.routes_puzzle import *
from Gamebook.src.routes_dice import *


from flask import Flask, render_template, request, url_for, redirect, flash, session



#### GROUP MAINS ####

# Group page
@app.route("/group/<string:group_id>", methods=["GET", "POST"])
def group(group_id):
  
    if check_key(session['username'], session['key']):
      group = load_group(group_id)
      
      static = 'group.html'
      return render_template(static, page=page_html(static, "in"), 
                            descriptions=descriptions, modes=modes, 
                            group=group)
    else:
      init_session()
      return redirect(url_for('login', retry=False))


# enter GameBook
@app.route("/gamebook")
def enter_gamebook():
  
  if check_key(session['username'], session['key']):    
    return redirect(f"/gamebook/{session['username']}")
  
  else: 
    init_session()
  
    return redirect(url_for('login', retry=False))


# GameBook
@app.route("/gamebook/<string:group_id>", methods=["GET", "POST"])
def gamebook(group_id):
  
  if check_key(session['username'], session['key']):
    group = load_group(group_id)
    
    stats = [[0 for _ in range(group.n + 1)] for _ in modes]
    for m, mode in enumerate(modes):
      
      games = group.results[group.results.g_mode == mode]
      n_games = games.shape[0]
      print('>> num games in category', mode, ':', n_games)
      if n_games > 0:
        wins = [n_games, *[games[games.winner_name == p].shape[0] for p in group.players]]
        stats[m] = wins
    
    static = 'gamebook.html'  
    return render_template(static, page=page_html(static, "in"),
                           descriptions=descriptions, modes=modes, 
                           group=group, giphs=mode_giphs, stats=stats,
                           num_modes=len(modes), mode_key=mode_key)
    
  else: 
    init_session()
  
    return redirect(url_for('login', retry=False))
  
  
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

  static = 'random.html'
  return render_template(static, page=page_html(static, "out"), 
                         modes=modes, descriptions=descriptions,
                         random_form=random_form)
  
  
# Start game
@app.route("/start/<string:mode>/<string:group_id>",  methods=["GET", "POST"])
def game_start(group_id, mode):
  
  session['round'] =    0
  check =               check_key(session['username'], session['key']) and (session['status'] == 'IN')
  
  if mode in ['rounds']:
    game_id =             gen_game_id(mode)
    session['game_id'] =  game_id
    if group_id=='random' or check:
      return redirect(f"/rounds/{group_id}/{game_id}/0")
    
  if mode in ['dice'] and check:
    game_id =             gen_game_id(mode)
    session['game_id'] =  game_id
    return redirect(f"/{mode}/{group_id}/{game_id}/start")
  
  if mode == 'puzzle' and check:
    return redirect(f"/puzzle/{group_id}/0")
  
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
          return redirect(url_for('login', retry=True))
        
  static = 'group_login.html'    
  return render_template(static, page=page_html(static, "out"), 
                         retry=retry)


# Logout
@app.route('/logout')
def logout():
   init_session()
   return redirect(f"/")


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
  
  static = 'group_create.html'  
  return render_template(static, page=page_html(static, "out"), 
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
  
  static = 'group_delete.html'
  return render_template(static, page=page_html(static, "out"), 
                         group_name=group_name, delete_form=delete_form)


# Motto
@app.route('/motto', methods=["GET", "POST"])
def motto():
  
  if check_key(session['username'], session['key']):
    
    group = load_group(session['username'])
    motto_form = MottoForm(csrf_enabled=False)
  
    if motto_form.validate_on_submit():
      
          group.motto = motto_form.motto.data
          group.update_group()
          return redirect(f'/group/{group.id}')

    static = 'group_motto.html'
    return render_template(static, page=page_html(static, "in"), 
                         group=group, motto_form=motto_form)
  
  else: redirect('/')