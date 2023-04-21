
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, IntegerField
from wtforms.validators import DataRequired



##### GROUP #####

# Registration 
class GroupForm(FlaskForm):
  
  name =  StringField("Group Name", validators=[DataRequired()])
  key =  StringField("Group Key", validators=[DataRequired()])
  motto = TextAreaField("What is your motto?")  
  
  p1 = StringField("Player 1", validators=[DataRequired()])
  p2 = StringField("Player 2", validators=[DataRequired()])
  p3 = StringField("Player 3")
  p4 = StringField("Player 4")
  p5 = StringField("Player 5")
  p6 = StringField("Player 6")
  p7 = StringField("Player 7")
  p8 = StringField("Player 8")
  
  submit = SubmitField("Save this group and proceed")


# delete
class DeleteForm(FlaskForm):
  key = StringField("Group Key", validators=[DataRequired()])
  submit = SubmitField("Delete this group and its GameBook")

# motto
class MottoForm(FlaskForm):
  motto = StringField("New motto", validators=[DataRequired()])
  submit = SubmitField("Change Motto")

  
#### GAME ####

# One Round
class CloseRoundForm(FlaskForm):
  
  pt1 = IntegerField("enter points", validators=[DataRequired()])
  pt2 = IntegerField("enter points", validators=[DataRequired()])
  pt3 = IntegerField("enter points")
  pt4 = IntegerField("enter points")
  pt5 = IntegerField("enter points")
  pt6 = IntegerField("enter points")
  pt7 = IntegerField("enter points")
  pt8 = IntegerField("enter points")
  
  submit = SubmitField("Close this Round")

# Submit Game
class SubmitGameForm(FlaskForm):
  info = TextAreaField("Page Comment", validators=[DataRequired()])
  submit = SubmitField("Finish this Page")
  
# Clear Game
class ClearGameForm(FlaskForm):
  submit = SubmitField("Reset your current Page")

# random_start 
class RandomGroup(FlaskForm):
  
  p1 = StringField("Player 1", validators=[DataRequired()])
  p2 = StringField("Player 2", validators=[DataRequired()])
  p3 = StringField("Player 3")
  p4 = StringField("Player 4")
  
  submit = SubmitField("Start without Login")