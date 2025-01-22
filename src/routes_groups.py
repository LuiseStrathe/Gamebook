
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


from flask import Flask, render_template, request, \
  url_for, redirect, flash, session
from flask_login import LoginManager






###############################################
#                     GROUP 
###############################################



# Group page

@app.route("/group/<string:group_id>", methods=["GET", "POST"])
def group(group_id):
  
  
    if check_key(session['username'], session['key']):
      group = load_group(group_id)[0]
      
      
      static = 'group.html'
      return render_template(
        static, page=page_html(static, "in"), 
        modes=modes_info, 
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




# Statistics  

@app.route("/gamebook/<string:group_id>", methods=["GET", "POST"])
def gamebook(group_id):
  
  if check_key(session['username'], session['key']):
    group = load_group(group_id)[0]
    
    stats = [[0 for _ in range(group.n + 1)] for _ in modes]
    for m, mode in enumerate(modes):
      
      games = group.results[group.results.g_mode == mode]
      n_games = games.shape[0]
      print('>> num games in category', mode, ':', n_games)
      if n_games > 0:
        wins = [n_games, *[games[games.winner_name == p].shape[0] for p in group.players]]
        stats[m] = wins
    
    static = 'gamebook.html'  
    return render_template(
      static, page=page_html(static, "in"),
      modes=modes_info, 
      group=group, stats=stats,
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
  return render_template(
    static, page=page_html(static, "out"), 
    modes=modes_info,
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



###############################################
#                     ADMIN 
###############################################



# Login

@app.route('/login', methods = ['GET', 'POST'])
def login():
  
  if 'retry' in request.args:
    retry = request.args['retry']
  else: retry = False
  
  if request.method == 'POST':
    
      name, key = request.form['username'], request.form['key']
      
      id = name_to_id(name)
      key = encrypt_key(key)
      
      if check_key(id, key):

          session['username'] = id
          session['key'] = key
          session['status'] = 'IN'
          session['num_players'] = load_group(id)[0].n
          session['round'] = 0
          session['game_id'] = 0
          
          print(name, 'is now logged in')

          return redirect(f"/group/{id}")
          
        
      else: 
          init_session()
          return redirect(url_for('login', retry=True))
        
  static = 'group_login.html'    
  return render_template(
    static, page=page_html(static, "out"), 
    retry=retry)




# Logout

@app.route('/logout')
def logout():
  
  if session['status'] == 'IN':
    session.pop(session['username'], None)
  
  init_session()
  
  return redirect(f"/")



# Register

@app.route("/register", methods=["GET", "POST"])
def register():
  
  group_form = GroupForm(csrf_enabled=False)
  
  if group_form.validate_on_submit():  
    
    name = group_form.name.data
    check, id = check_name(name)  
        
    if check:
      
      players, colors = create_players(group_form)
      
      group = My_Group(
        name=group_form.name.data, 
        slogan=group_form.slogan.data,
        key=group_form.key.data, 
        players=players, colors=colors)
      
      session['username'] = group.id
      session['key'] = group.key
      session['num_players'] = group.n
      session['status'] = 'IN'
      
      return redirect(f"/group/{group.id}")
    
    else: print("ERROR: group probably arleady exists")
  
  static = 'group_register.html'  
  return render_template(
    static, page=page_html(static, "out"), 
    group_form=group_form)






# Settings

@app.route('/settings', methods=["GET", "POST"])
def settings():
  
  
  if check_key(session['username'], session['key']):
  
    # init page  
    group = load_group(session['username'])[0]
    info = ""
    static = 'group_settings.html'
    
    settings_form = SettingsForm(csrf_enabled=False)
    delete_form = DeleteForm(csrf_enabled=False)    
      
  
    # update settings
    if settings_form.validate_on_submit():
      
      key = encrypt_key(settings_form.changePassword.data)
      print('Settings submitted:')
      print(' > key: ', key)
      
      if check_key(group.id, key):

        group = group.update_settings(settings_form)
        group.update_group()
        
        return redirect('/settings') 
        
      else: 
        info = "Wrong password"
      
    else: 
      print(settings_form.errors)

    
    # delete group
    if delete_form.validate_on_submit():    
      
      key = encrypt_key(delete_form.deletePassword.data)
      
      if check_key(group.id, key):

        delete_group(group.id)
        init_session()
        
        return redirect('/') 
      
      else: 
        info = "Wrong password"
                  

    return render_template(
      static, page=page_html(static, "in"), 
      group=group, info=info,
      settings_form=settings_form, 
      delete_form=delete_form)
  
  else: redirect('/')
  
  