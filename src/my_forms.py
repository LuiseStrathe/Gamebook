
from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, \
  BooleanField, RadioField, IntegerField, SelectMultipleField, \
  SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, \
  EqualTo, ValidationError

from Gamebook.src.my_params import player_colors




############################################

#                   ADMIN 
                     
############################################


class GroupForm(FlaskForm):
  
  name =        StringField("Group Name", 
    validators=[DataRequired(), Length(max=20)])
  
  key =         PasswordField("Group Key", 
    validators=[DataRequired(), Length(min=5, max=20)])
  
  key_confirm = PasswordField("Confirm Key", 
    validators= [DataRequired(), EqualTo('key'), Length(min=5, max=20)])
  
  slogan =      TextAreaField("slogan")  
  
  num =         IntegerField("Number of Players",)
  
  p0 = StringField("Player 1", 
    validators=[DataRequired(), Length(max=20)])
  p1 = StringField("Player 2", 
    validators=[DataRequired(), Length(max=20)])
  p2 = StringField("Player 3", validators=[Length(max=20)])
  p3 = StringField("Player 4", validators=[Length(max=20)])
  p4 = StringField("Player 5", validators=[Length(max=20)])
  p5 = StringField("Player 6", validators=[Length(max=20)])
  p6 = StringField("Player 7", validators=[Length(max=20)])
  p7 = StringField("Player 8", validators=[Length(max=20)])
  p8 = StringField("Player 9", validators=[Length(max=20)])
  p9 = StringField("Player 10", validators=[Length(max=20)])
  
  c0 = SelectField("c0", choices=player_colors,)
  c1 = SelectField("c1", choices=player_colors,)
  c2 = SelectField("c2", choices=player_colors,)
  c3 = SelectField("c3", choices=player_colors,)
  c4 = SelectField("c4", choices=player_colors,)
  c5 = SelectField("c5", choices=player_colors,)
  c6 = SelectField("c6", choices=player_colors,)
  c7 = SelectField("c7", choices=player_colors,)
  c8 = SelectField("c8", choices=player_colors,)
  c9 = SelectField("c9", choices=player_colors,)
  
  registration_submit = SubmitField("Register this Group")



# Settings
class SettingsForm(FlaskForm):
  
  slogan = TextAreaField("slogan")
  
  # Player names
  p0 = StringField("p0", 
    validators=[Length(max=20)])
  p1 = StringField("p1", 
    validators=[Length(max=20)])
  p2 = StringField("p2", 
    validators=[Length(max=20)])
  p3 = StringField("p3", 
    validators=[Length(max=20)])
  p4 = StringField("p4", 
    validators=[Length(max=20)])
  p5 = StringField("p5", 
    validators=[Length(max=20)])
  p6 = StringField("p6", 
    validators=[Length(max=20)])
  p7 = StringField("p7", 
    validators=[Length(max=20)])
  p8 = StringField("p8", 
    validators=[Length(max=20)])
  p9 = StringField("p9", 
    validators=[Length(max=20)])
  pNew = StringField("pNew", 
    validators=[Length(max=20)])
  
  # Color selection
  c0 = SelectField("c0", choices=player_colors, default="#cabc22")
  c1 = SelectField("c1", choices=player_colors, default="#cabc22")
  c2 = SelectField("c2", choices=player_colors, default="#cabc22")
  c3 = SelectField("c3", choices=player_colors, default="#cabc22")
  c4 = SelectField("c4", choices=player_colors, default="#cabc22")
  c5 = SelectField("c5", choices=player_colors, default="#cabc22")
  c6 = SelectField("c6", choices=player_colors, default="#cabc22")
  c7 = SelectField("c7", choices=player_colors, default="#cabc22")
  c8 = SelectField("c8", choices=player_colors, default="#cabc22")
  c9 = SelectField("c9", choices=player_colors, default="#cabc22")
  cNew = SelectField(u"cNew", choices=player_colors, default="#cabc22")
  
  # Check for color change
  x0 = BooleanField("x_c0")
  x1 = BooleanField("x_c1")
  x2 = BooleanField("x_c2")
  x3 = BooleanField("x_c3")
  x4 = BooleanField("x_c4")
  x5 = BooleanField("x_c5")
  x6 = BooleanField("x_c6")
  x7 = BooleanField("x_c7")
  x8 = BooleanField("x_c8")
  x9 = BooleanField("x_c9")
  xNew = BooleanField("x_cNew")
  
  
  changePassword = PasswordField("changePassword", 
    validators=[DataRequired()])
  settings_submit = SubmitField("Save Changes")



# Delete Group
class DeleteForm(FlaskForm):
  
  deletePassword = PasswordField("deletePassword", 
    validators=[DataRequired()])
  delete_submit = SubmitField("DELETE")




  
  
############################################

#                    GAMES 
                     
############################################



# ROUNDS

class StartRoundsForm(FlaskForm):
  
  r_title = StringField("Rounds Game Title", 
    validators=[DataRequired(), Length(min=3, max=20)])
  
  r_p_0 = BooleanField("Rounds Player 1")
  r_p_1 = BooleanField("Rounds Player 2")
  r_p_2 = BooleanField("Rounds Player 3")
  r_p_3 = BooleanField("Rounds Player 4")
  r_p_4 = BooleanField("Rounds Player 5")
  r_p_5 = BooleanField("Rounds Player 6")
  r_p_6 = BooleanField("Rounds Player 7")
  r_p_7 = BooleanField("Rounds Player 8")
  r_p_8 = BooleanField("Rounds Player 9")
  r_p_9 = BooleanField("Rounds Player 10")
  
  submit_rounds_start = SubmitField("Start Rounds")
  


class CloseRoundForm(FlaskForm):
  
  pt0 = IntegerField("enter points", validators=[DataRequired()])
  pt1 = IntegerField("enter points", validators=[DataRequired()])
  pt2 = IntegerField("enter points")
  pt3 = IntegerField("enter points")
  pt4 = IntegerField("enter points")
  pt5 = IntegerField("enter points")
  pt6 = IntegerField("enter points")
  pt7 = IntegerField("enter points")
  pt8 = IntegerField("enter points")
  pt9 = IntegerField("enter points")
  
  r_comment = TextAreaField("Comment (optional)")
  
  submit = SubmitField("Close Round")


  
# PUZZLE

class AddPuzzleForm(FlaskForm):
  
  title = StringField("Title", 
                      validators=[DataRequired(), Length(min=3, max=20)])
  pcs = IntegerField("Number of Pieces", 
                     validators=[DataRequired()])
  description = StringField("Description (optional)")
  
  submit_add_puzzle = SubmitField("Add Puzzle")
  
  
  
class ChangePuzzleForm(FlaskForm):
  
  puzzle_change = SelectField("Puzzle change", 
    choices=[], validators=[DataRequired()])
  title_change = StringField("Title change")
  description_change = StringField("Description change")
  delete = BooleanField("Delete")
  
  submit_change_puzzle = SubmitField("Submit Changes")
  
  def __init__(self, puzzles, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.puzzle_change.choices = puzzles
  
  
  
class PuzzleRecordForm(FlaskForm):
  player = SelectField("Player", 
    choices=[], validators=[DataRequired()])
  puzzle = SelectField("Puzzle ID",
    choices=[], validators=[DataRequired()])
  hours = IntegerField("Hours", default=0)
  minutes = IntegerField("Minutes", default=0, validators=[DataRequired()])
  seconds = IntegerField("Seconds", default=0)
  comment = StringField("Comment (optional)")
  submit_puzzle_log = SubmitField("Save Log")
  
  def __init__(self, players, choice_puzzles, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.puzzle.choices = choice_puzzles
    self.player.choices = players






############################################

#                    OLD 
                     
############################################



# Submit Game
class SubmitGameForm(FlaskForm):
  
  info = TextAreaField("Page Comment", validators=[DataRequired()])
  submit = SubmitField("Finish this Page")



# random_start 
class RandomGroup(FlaskForm):
  
  p1 = StringField("Player 1", validators=[DataRequired()])
  p2 = StringField("Player 2", validators=[DataRequired()])
  p3 = StringField("Player 3")
  p4 = StringField("Player 4")
  
  submit = SubmitField("Start without Login")
  
  
  
