from flask import Flask
from data.server.secret import secret_key
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


import src.routes
import src.routes_rounds
import src.routes_groups


if __name__ == "__main__":
	app.run()