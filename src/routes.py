
import sys
sys.path.insert(1, "./")
from Gamebook.gamebook_app import app

from Gamebook.src.my_forms import *
from Gamebook.src.my_params import *
from Gamebook.src.my_classes import *
from Gamebook.src.my_fun import *
from Gamebook.src.routes_rounds import *
from Gamebook.src.routes_groups import *


from flask import Flask, render_template, request, url_for, redirect, flash, session





# INDEX
@app.route("/")
def index():
  
  if session['status'] == 'IN':
    
    username = session['username']
    id = name_to_id(username)
    
    group = load_group(id)
    return redirect(f'/group/{group.id}')
  
  init_session()
  
  static = "_index.html"
  return render_template(static, page=page_html(static, "out"),
                         modes=modes, descriptions=descriptions, 
                         about_info=about_info, giphs=mode_giphs,
                         num_modes=len(modes))



# about
@app.route("/about")
def about():
 
  static = "_about.html"
  return render_template(static, page=page_html(static),
                         about_info=about_info)



# ERRORS
@app.errorhandler(400) 
def not_found0(e): 
  return render_template("_400.html") 


@app.errorhandler(404) 
def not_found1(e): 
  return render_template("_404.html") 


@app.errorhandler(500) 
def not_found2(e): 
  return render_template("_404.html") 