
import sys
sys.path.insert(1, "./")
from Gamebook.gamebook_app import app

from Gamebook.src.my_forms import *
from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *
from Gamebook.src.my_fun import *
from Gamebook.src.routes_rounds import *
from Gamebook.src.routes_groups import *


from flask import Flask, render_template, \
  request, url_for, redirect, flash, session
from flask_login import LoginManager




################  SESSION  ###############


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  
    return User.get(user_id)
  
  
  

#################  MAIN  #################


# INDEX
@app.route("/")
def index():
  
  if verify_session():
    id = name_to_id(session['username'])
    
    return redirect(f'/group/{id}')
  
  init_session()
  
  static = "_index.html"
  return render_template(static, page=page_html(static, "out"),
                         modes=modes, descriptions=descriptions, 
                         about_info=about_info, giphs=mode_giphs,
                         num_modes=len(modes))



# ABOUT
@app.route("/about")
def about():
 
  static = "_about.html"
  return render_template(static, page=page_html(static),
                         about_info=about_info)



#################  ERRORS  #################


# Page not found
@app.errorhandler(404) 
def not_found_page(e): 
  return render_template("_404.html") 


# Bad request - user input/page request
@app.errorhandler(400) 
def error400(e): 
  return render_template("error.html") 

# Unauthorized
@app.errorhandler(401) 
def error401(e): 
  return render_template("error.html") 


# Method not allowed
@app.errorhandler(405) 
def error405(e): 
  return render_template("error.html") 

# Request Timeout
@app.errorhandler(408) 
def error408(e): 
  return render_template("error.html") 