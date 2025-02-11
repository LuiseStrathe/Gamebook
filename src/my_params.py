
# This file contains all the parameters that are 
# used in the GameBook application.


# Content:

#   > General
#   > Data
#   > Modes
#   > Texts (What is GamesBook)





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
    "stats_rounds.html": "Stats",
    "stats_dice.html": "Stats",
    "stats_puzzle.html": "Stats",
    "dice.html": "Dice",
    "puzzle.html": "Puzzles",
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

chart_colors = [
    '#d04fa1', '#007c59', '#cf7437', '#25b922', '#cabc22',
    '#b21a1a', '#3925a5', '#228ad0', '#8a37a0', '#31b1b5',
    '#df5e6b', '#ff8c00', '#ff1493', '#ff4500', '#ff6347',
    '#ff69b4', '#ff7f50', '#ff8c00', '#ff00ff', '#ff1493',
    '#ff4500', '#ff6347', '#ff69b4', '#ff7f50', '#ff8c00',
    '#ff00ff', '#ff1493', '#ff4500', '#ff6347', '#ff69b4',
    '#ff7f50', '#ff8c00', '#ff00ff', '#ff1493', '#ff4500',
    '#ff6347', '#ff69b4', '#ff7f50', '#ff8c00', '#ff00ff',
    '#ff1493', '#ff4500', '#ff6347', '#ff69b4', '#ff7f50',
    '#ff8c00', '#ff00ff', '#ff1493', '#ff4500', '#ff6347',
    '#ff69b4', '#ff7f50', '#ff8c00', '#ff00ff', '#ff1493',
    '#ff4500', '#ff6347', '#ff69b4', '#ff7f50', '#ff8c00',
    '#ff00ff', '#ff1493', '#ff4500', '#ff6347', '#ff69b4',
    '#ff7f50', '#ff8c00', '#ff00ff', '#ff1493', '#ff4500',
    '#ff6347', '#ff69b4', '#ff7f50', '#ff8c00', '#ff00ff',]
           
            
puzzle_cols = ['id', 'title', 'description', 'pcs'] 

dice_rows = [
    "1's", "2's", "3's", "4's", "5's", "6's", '3 of a kind',
    '4 of a kind', 'full house', 'small straight', 
    'large straight', 'YEAHA', 'chance']




#############  MODES  ################


modes = ["rounds", "dice", 'puzzle']


mode_key = {"rounds": "R", "dice": "D", "puzzle": "P"}


# [0:mode_name, 1:description_short, 2:description_long, 3:description_img, 
#  4:icon white, 5:icon, 6:giphy]

modes_info = [
    ["rounds", 
        
        "Play round-based games within your group.", 
        
        "Play round-based games within your group.\n\n \
        In each round, you can enter points for each player.\n \
        The winner is the player with the most points over all rounds.\n\n \
        You can use this mode for all kinds of games. Either you note down rounds \
        (as in scrabble) or \
        the results of multiple games you want to combine, e.g. cards or table tennis.",
        
        "../static/media/modes/desc_mode.png", 
        "../static/media/modes/rounds_icon_tr.png", 
        "../static/media/modes/rounds_icon.png", 
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
        "../static/media/modes/dice_icon_tr.png", 
        "../static/media/modes/dice_icon.png", 
        'https://giphy.com/embed/l2JdUMnCDg6qs368g',
    ],
    
    ["puzzle",
     
        "Save the puzzles you've finished and compare times.",
        
        "Challenge your puzzle skills: \
        finish a puzzle tracking the time you need to finish it. \
        You can then log your time in GamesBook in a easy way. \
        Just add the puzzle once and then save logs each time you finish it. \n \
        After a view entries you will be able to explore your stats  \
        and compare within your group.",        
        
        "../static/media/modes/desc_mode.png", 
        "../static/media/modes/puzzle_icon_tr.png",
        "../static/media/modes/puzzle_icon.png",
        'https://giphy.com/embed/3o6Mbr1blVD5KKQBxK',
    ],
]      





#############  TEXTS  ################



about_info = \
    [   # index
        "You enjoy playing games with your friends irl? \
        You want to keep track of your scores and analyze them? \
        Then GamesBook is the right place for you.",
        
        "GamesBook is a simple and free notebook for game results. \
        It allows you to save, share and analyize games you play with friends. \n \n \
        You can create a shared group account for up to 10 players,  \
        to then add logs with the results of the games you played with the group. \
        Now you have access to all of the group's games and analytics \
        in GamesBook to never lose track of scores again. \n ",

        # about
        "GamesBook is a simple and free notebook for game results. \
        It allows you to save, share and analyize games you play with friends. \n\n \
        You can create a shared group account for up to 10 players,  \
        to then add logs with the results of the games you played with the group. \
        Now you have access to all of the group's games and analytics \
        in GamesBook to never lose track of scores again.",
        
        "You can use GamesBook for all kinds of games. \
        For most games you would choose 'Rounds' which simply represents \
        round-based games or even just the winner and participants of a game. \n \
        Feel free to create several groups to separate their logs as they belong. \n ",
]