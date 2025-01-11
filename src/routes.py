
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
    group = load_group(session['group_id'])
    return redirect(f'/group/{group.id}')
  
  init_session()
  
  return render_template("_index.html", 
                         modes=modes, descriptions=descriptions, 
                         about_info=about_info, giphs=mode_giphs,
                         num_modes=len(modes), head="__head_out.html")



# about
@app.route("/about")
def about():
  
  head_html = get_head_html()
  return render_template("_about.html", about_info=about_info, 
                         head=head_html)



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