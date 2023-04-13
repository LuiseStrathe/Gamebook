from flask import Flask, render_template, request
from helper import *
from forms import *
from app import app, db



#### INDEX ####

@app.route("/")
def index():
  return render_template("index.html", games=games, descriptions=descriptions)



#### GAMEPAGE ####

@app.route("/basic/<int:n>", methods=["GET", "POST"])
def basic(n):
  player_form = PlayerForm4(csrf_enabled=False)
  if player_form.validate_on_submit():
    #players = player_form[0].data, player_form[1].data, player_form[2].data, player_form[3].data
    id = 42
    return render_template("/basic/game_42.html", id=id)
  return render_template("basic.html", player_form=player_form, 
                         n=n)


@app.route("/basic/game_<int:id>", methods=["GET", "POST"])
def basic_book(id):
  return render_template("basic_game.html")



#### ELSE ####

@app.route("/about")
def about():
  return render_template("about.html")

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

@app.errorhandler(500) 
def not_found(e): 
  return render_template("404.html") 