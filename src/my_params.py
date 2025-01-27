
# This file contains all the parameters that are 
# used in the GameBook application.


# Content:

#   > General
#   > Data
#   > Modes
#   > Texts





#############  GENERAL  ##############



path_data = 'data/'

page_titles = {
    "_about.html": "About",
    "group_register.html": "Register",
    "group_login.html": "Login",
    "group_settings.html": "Settings",
    "group.html": "Overview",    
    "_index.html": "Home",
    "stats.html": "Stats",
    
    "dice_page.html": "Dice",
    "dice_start.html": "Dice",
    "dice.html": "Dice",
    "puzzle.html": "Puzzles",
    "puzzle_stats.html": "Stats",
    "random.html": "Test GamesBook",
    "rounds_page.html": "Rounds",
    "rounds.html": "Rounds",
}





#############  DATA  ################


result_cols = ['game_id', 'g_mode', "group_id",
               "result", "n_rounds", "winner_name", 'time', 
               'info_1', 'info_2', 'info_3']

'''         result: np array of points, mode specific scheme
            time:   timestamp
            info:   mode specific info
'''
     

player_cols = ['name', 'color', 'icon', 'info']     
         

player_colors = [
    ('#d04fa1', 'Pink'),
    ('#007c59', 'Dark Green'), 
    ('#cf7437', 'Orange'),
    ('#25b922', 'Green'),
    ('#cabc22', 'Yellow'),
    ('#b21a1a', 'Red'),
    ('#3925a5', 'Dark Blue'),
    ('#228ad0', 'Blue'),
    ('#8a37a0', 'Violet'),
    ('#31b1b5', 'Turquoise'),
    ('#df5e6b', 'Light Red'),
]
           
            
puzzle_cols = ['id', 'title', 'description', 'pcs'] 

dice_rows = [
    "1's", "2's", "3's", "4's", "5's", "6's", '3 of a kind',
    '4 of a kind', 'full house', 'small straight', 
    'large straight', 'YEAHA', 'chance']




#############  MODES  ################


modes = ["rounds", "dice", 'puzzle', 'skat']


mode_key = {"rounds": "R", "dice": "D", "puzzle": "P", "skat": "S"}


# [0:mode_name, 1:description_short, 2:description_long, 3:description_img, 
#  4:icon, 5:scheme, 6:giphy]

modes_info = [
    ["rounds", 
        
        "Play round-based games within your group.", 
        
        "This game mode is not yet available.\n\n \
        Play round-based games within your group.\n\n \
        In each round, you can enter points for each player.\n \
        The winner is the player with the most points over all rounds.\n\n \
        You can use this mode for all kinds of games. Either you note down rounds \
        (as in scrabble) or \
        the results of multiple games you want to combine, e.g. cards or table tennis.",
        
        "../static/media/modes/desc_mode.png", 
        "&#x270E;",
        "../static/media/modes/scheme_rounds.png", 
        "https://giphy.com/embed/3tEFVAbfzzcwo",
    ],
    
    ["dice",
     
        "Roll 5 dice to gain points for specific combinations.",
        
        "This game mode is not yet available.\n\n \
        Roll the dice and as in the classic achieve points in different categories. \n\n \
        You need 5 Dice. The acitve player can reroll twice.\n \
        Each time you roll the dice, you can choose which dice you want to keep. \
        You can not reroll with those anymore.\n \
        To end your turn you have to choose a combination and gain the points.\n \
        The winner is the player with most points in total.",
        
        "../static/media/modes/desc_mode.png",  
        "&#x2682;",
        "../static/media/modes/scheme_dice.png", 
        'https://giphy.com/embed/l2JdUMnCDg6qs368g',
    ],
    
    ["puzzle",
     
        "Save the puzzles you've finished and compare times.",
        
        "Test your puzzle skills\n\n \
        Finish a puzzle tracking the time you need to finish it. \
        You can then log your time in GamesBook in a easy way. \
        Just add the puzzle once and save logs for the times you finished it. \n \
        After a view entries you will be able to explore your stats  \
        and compare within your group.",        
        
        "../static/media/modes/desc_mode.png", 
        "&#x1F9E9;",
        "../static/media/modes/scheme_puzzle.png",
        'https://giphy.com/embed/3o6Mbr1blVD5KKQBxK',
    ],
    
    ["skat",
     
        "Cards game for 3 to 4 players.",
        
        "This game mode is not yet available.\n\n \
        Play with your 32 cards set and 3 to 4 players.\n \
        After each round, the winners ponts will be updated.",
        
        "../static/media/modes/desc_mode.png", 
        "&#x1F0D4;",
        "../static/media/modes/scheme_rounds.png", 
        'https://giphy.com/embed/3o7btPCcdNniyf0ArS',
    ],
]      





#############  TEXTS  ################



about_info = \
    "This GameBook is a simple and free online game notebook. \
    You might have an analogue game book at home. \n\n \
    GamesBook a simple web application that allows you to save logs \
    of the games you play with others and even analyze them later on. \n\n \
    You can create a shared group account for up to 10 players. \
    Each game you play will add a log to your GamesBook with the final results. \
    This way you have access to statistics of all your group's games \
    and never lose track of the scores again. \n "

                
    