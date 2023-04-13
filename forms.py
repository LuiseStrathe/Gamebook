
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class BasicForm(FlaskForm):
  round =  StringField("Round", validators=[DataRequired()])
  close_round = SubmitField("Close this Round")

class PlayerForm4(FlaskForm):
  p1 = StringField("Player 1", validators=[DataRequired()])
  p2 = StringField("Player 2", validators=[DataRequired()])
  p3 = StringField("Player 3", validators=[DataRequired()])
  p4 = StringField("Player 4", validators=[DataRequired()])
  submit = SubmitField("Start new Game")
  
