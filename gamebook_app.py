from data.server.secret import secret_key
import sys
sys.path.append("./")

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == "__main__":
	app.run()
 
 
 
import Gamebook.src.routes
import Gamebook.src.routes_rounds
import Gamebook.src.routes_groups
import Gamebook.src.routes_puzzle
import Gamebook.src.routes_dice