
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
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
  
  submit = SubmitField("Save this group and proceed")


# delete
class DeleteForm(FlaskForm):
  key = StringField("Group Key", validators=[DataRequired()])
  submit = SubmitField("Delete this group and its GameBook")



  
#### GAME ####

# One Round
class CloseRoundForm(FlaskForm):
  submit = SubmitField("Close this Round")

# Submit Game
class SubmitGameForm(FlaskForm):
  submit = SubmitField("Finish this Game")
  
# Clear Game
class ClearGameForm(FlaskForm):
  submit = SubmitField("Reset your current Game")

