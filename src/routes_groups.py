
import sys
sys.path.insert(1, "./")
from Gamebook.gamebook_app import app

from Gamebook.src.my_forms import *
from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *
from Gamebook.src.my_fun import *
from Gamebook.src.routes import *
from Gamebook.src.routes_rounds import *
from Gamebook.src.routes_puzzles import *
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
    
    info = ""
    rounds_form = StartRoundsForm(csrf_enabled=False)
    dice_form = StartDiceForm(csrf_enabled=False)
    
    
    if rounds_form.validate_on_submit():          
      game_id, info = start_rounds(group_id, rounds_form)
      
      if info == '':      
        return redirect(f"/rounds/{game_id}")
    
    else: print("> Submit ROUNDS - errors:", rounds_form.errors)
    
    
    if dice_form.validate_on_submit():
      game_id, info = start_dice(group_id, dice_form)
      
      if info == '':      
        return redirect(f"/dice/{game_id}")
      
    else: print("> Submit DICE - errors:", dice_form.errors)
    
    
    static = 'group.html'
    return render_template(
      static, page=page_html(static, "IN"), info=info,
      modes=modes_info, num_modes=len(modes), group=group, 
      rounds_form=rounds_form, dice_form=dice_form)
    
    
  else:
    init_session()
    return redirect(url_for('login', retry=False))






# Statistics  

@app.route("/statistics", methods=["GET", "POST"])
def statistics():
  
  if (verify_session() == False) or \
    not(check_key(session['username'], session['key'])):
      init_session()
      return redirect(url_for('login', retry=False))  
    
      
  static = 'stats.html'  
  return render_template(
    static, page=page_html(static, "IN"),
    modes=modes, modes_info=modes_info,)
    




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

          return redirect(f"/group/{id}")
          
        
      else: 
          init_session()
          return redirect(url_for('login', retry=True))
        
  static = 'group_login.html'    
  return render_template(
    static, page=page_html(static, "no"), 
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
  info = ""
  
  if group_form.validate_on_submit():  
    
    # check if group name
    name = str(group_form.name.data)
    
    check, id = check_name(name)    
    if check:
      players, colors = create_players(group_form)
    
      if len(players) == len(set(players)):
      
        group = My_Group(
          name=group_form.name.data, 
          slogan=group_form.slogan.data,
          key=group_form.key.data, 
          players=players, colors=colors)
        
        session['username'] = group.id
        session['key'] = group.key
        session['status'] = 'IN'
        
        return redirect(f"/group/{group.id}")
      
      else: info = "The players' names should be unique"
    else: info="This group name arleady exists"
  
  static = 'group_register.html'  
  return render_template(
    static, page=page_html(static, "no"), 
    group_form=group_form, info=info)






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
      
      if check_key(group.id, key):

        group = group.update_settings(settings_form)
        
        if group == False:
          info = 'The player names must be unique'
          group = load_group(session['username'])[0]
          
        else:
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
      static, page=page_html(static, "IN"), 
      group=group, info=info,
      settings_form=settings_form, 
      delete_form=delete_form)
  
  else: redirect('/')
  
  