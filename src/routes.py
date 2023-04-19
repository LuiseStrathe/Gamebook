
import sys
sys.path.insert(1, "./")
from app import app

from src.my_forms import *
from src.my_params import *
from src.my_classes import *
from src.my_fun import *
from src.routes_rounds import *
from src.routes_groups import *


from flask import Flask, render_template, request, url_for, redirect, flash, session



# INDEX
@app.route("/")
def index():
  
  if ('username' in session) and \
      check_key(session['username'], session['key']):
      session['status'] = 'IN'
      return redirect('group/' + session['username'])
  else: init_session()
  
  return render_template("_index.html", 
                         modes=modes, descriptions=descriptions, 
                         about_info=about_info, giphs=mode_giphs,
                         num_modes=len(modes))



# about
@app.route("/about")
def about():
  base = get_base()
  return render_template("_about.html", base=base,
                         about_info=about_info)



# ERRORS
@app.errorhandler(400) 
def not_found(e): 
  base = get_base()
  return render_template("_400.html", base=base) 

@app.errorhandler(404) 
def not_found(e): 
  base = get_base()
  return render_template("_404.html", base=base) 

@app.errorhandler(500) 
def not_found(e): 
  base = get_base()
  return render_template("_404.html", base=base) 