
from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, \
  BooleanField, RadioField, IntegerField, SelectMultipleField, \
  SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, \
  EqualTo, ValidationError, Optional, NumberRange

from Gamebook.src.my_params import player_colors, dice_rows




############################################

#                   ADMIN 
                     
############################################


class GroupForm(FlaskForm):
  
  name =        StringField("Group Name", 
    validators=[DataRequired(), Length(min=3, max=20)])
  
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
  
  for i in range(10):
    exec(f"c{i} = SelectField('c{i}', choices={player_colors})")
  
  registration_submit = SubmitField("Register")



# Settings
class SettingsForm(FlaskForm):
  
  slogan = TextAreaField("slogan")
  
  
  # Player names
  for i in range(10):
    exec(f"p{i} = StringField('p{i}', validators=[Length(max=20)])")

  pNew = StringField("pNew", 
    validators=[Length(max=20)])
  
  
  # Color selection
  for i in range(10):
    exec(f"c{i} = SelectField('c{i}', choices={player_colors}, default='#cabc22')")
 
  cNew = SelectField(u"cNew", choices=player_colors, default="#cabc22")
  
  
  # Check for color change
  for i in range(10):
    exec(f"x{i} = BooleanField('x_c{i}')")

  xNew = BooleanField("x_cNew")
  
  
  changePassword = PasswordField("changePassword", 
    validators=[DataRequired()])
  settings_submit = SubmitField("Save")



# Delete Group
class DeleteForm(FlaskForm):
  
  deletePassword = PasswordField("deletePassword", 
    validators=[DataRequired()])
  delete_submit = SubmitField("DELETE")




  
  
############################################

#                    GAMES 
                     
############################################


# SUBMIT Game, finally
class SubmitGameForm(FlaskForm):
  
  comment = TextAreaField("Comment", validators=[Optional()])
  submit = SubmitField("Save this Game", validators=[DataRequired()])



# ROUNDS

class StartRoundsForm(FlaskForm):
  
  r_title = StringField("Rounds Game Title", 
    validators=[DataRequired(), Length(min=3, max=20)])
  
  for i in range(10):   # 10 players
    exec(f"r_p_{i} = BooleanField('Rounds Player {i+1}')")
  
  submit_rounds_start = SubmitField("Start")
  


class CloseRoundForm(FlaskForm):
  
  for i in range(10):   # 10 players
    exec(f"pt{i} = IntegerField('enter points', validators=[Optional()])")
  
  submitRound = SubmitField("Confirm  ⏵  Next Round", validators=[DataRequired()])



# DICE

class StartDiceForm(FlaskForm):
  
  for i in range(10):   # 10 players
    exec(f"d_p_{i} = BooleanField('Dice Player {i+1}')")
  
  submit_dice_start = SubmitField("Start")



class PlayDiceForm(FlaskForm):
  
  for i in range(10):   # 10 players
    
    # x's & x of a kind values
    for j in range(8): 
      id, name = dice_rows[0][j], dice_rows[1][j]
      exec(f"p{i}_{id} = IntegerField('{name}', \
        validators=[Optional(strip_whitespace=True)])")
      
    # straights & full house & gamer
    for j in range(8, 12): 
      id, name = dice_rows[0][j], dice_rows[1][j]
      exec(f"p{i}_{id} = IntegerField('{name}', \
        validators=[Optional(strip_whitespace=True)])")
      
    # chance
    id, name = dice_rows[0][12], dice_rows[1][12]
    exec(f"p{i}_{id} = IntegerField('{name}', \
      validators=[Optional(strip_whitespace=True)])")
    
  submitDice = SubmitField("Confirm  ⏵  Next Round", validators=[DataRequired()])


  
# PUZZLE

class AddPuzzleForm(FlaskForm):
  
  title = StringField("Title", 
    validators=[DataRequired(), Length(min=3, max=20)])
  pcs = IntegerField("Number of Pieces", 
    validators=[DataRequired()])
  description = StringField("Description (optional)")
  
  submit_add_puzzle = SubmitField("Save")
  
  
  
class ChangePuzzleForm(FlaskForm):
  
  puzzle_change = SelectField("Puzzle change", 
    choices=[], validators=[DataRequired()])
  title_change = StringField("Title change")
  description_change = StringField("Description change")
  delete = BooleanField("Delete")
  
  submit_change_puzzle = SubmitField("Save")
  
  def __init__(self, puzzles, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.puzzle_change.choices = puzzles
  
  
  
class PuzzleRecordForm(FlaskForm):
  player = SelectField("Player", 
    choices=[], validators=[DataRequired()])
  puzzle = SelectField("Puzzle ID",
    choices=[], validators=[DataRequired()])
  hours = IntegerField("Hours", default=0, 
                validators=[NumberRange(min=0, max=1000)])
  minutes = IntegerField("Minutes", default=1, 
                validators=[DataRequired(), NumberRange(min=0, max=59)])
  seconds = IntegerField("Seconds", default=0, 
                validators=[NumberRange(min=0, max=59)])
  comment = StringField("Comment (optional)")
  submit_puzzle_log = SubmitField("Save")
  
  def __init__(self, players, choice_puzzles, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.puzzle.choices = choice_puzzles
    self.player.choices = players


class PuzzleRecordDeleteForm(FlaskForm):
  logs = SelectField("Logs", 
    choices=[], validators=[DataRequired()])
  submit_puzzle_log_delete = SubmitField("Delete")
  
  def __init__(self, log_choices, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.logs.choices = log_choices
    

class PuzzleLogFilterForm(FlaskForm):
  player = SelectField("Player", 
    choices=[], validators=[Optional()])
  size = SelectField("Size", 
    choices=[], validators=[Optional()])
  puzzle = SelectField("Puzzle", 
    choices=[], validators=[Optional()])
  date = SelectField("Date",
    choices=[], validators=[Optional()])
  apply_puzzle_log_filter = SubmitField("Filter")
  
  def __init__(self, choice_filter, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.player.choices = ['All Players'] + choice_filter[0]
    self.size.choices = ['All Sizes'] + choice_filter[1]
    self.puzzle.choices = ['All Puzzles'] + choice_filter[2]
    self.date.choices = ['All Times'] + choice_filter[3]
