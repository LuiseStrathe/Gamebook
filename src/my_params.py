
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
    "stats_puzzle_all.html": "Stats",
    "dice.html": "Dice",
    "puzzle.html": "Puzzles",
    "rounds.html": "Rounds",
}





#############  DATA  ################


result_cols = [
    'game_id', 'mode', 'group_id', 'time_stamp',     
    'g_data', 'n_rounds', 'title',     
    'player_ids', 'winner_id', 'comment',     
    'info_1', 'info_2', 'info_3']


''' 
    game_id:     unique id of game
    mode:      mode name ('rounds', 'dice', 'puzzle')
    timestamp:   timestamp of sevd log    
    
    g_data: list of all numeric results (points, times, etc.)
    n_rounds:    number of rounds played, pcs of puzzle respectively
    title:       title / category of game/puzzle
    
    combatants_id: list of player ids
    winner_id:   id of winner
    comment:     comment on game from input
    
    info:   mode specific info
    
    > players, puzzles and game titles identified by id, not string <
'''
     

player_cols = [
    'name', 'color', 'icon', 'info']     
         

player_colors = [
    ('#d04fa1', 'Pink'),
    ('#007c59', 'Dark Green'), 
    ('#cf7437', 'Orange'),
    ('#25b922', 'Green'),
    ('#cabc22', 'Yellow'),
    ('#b21a1a', 'Red'),
    ('#0a22f2', 'Dark Blue'),
    ('#228ad0', 'Blue'),
    ('#8a37a0', 'Violet'),
    ('#31b1b5', 'Turquoise'),
    ('#df5e6b', 'Light Red'),
]

chart_colors = [
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
           
            
puzzle_cols = [
    'id', 'title', 'description', 'pcs'] 

dice_rows = [
    ['1s', '2s', '3s', '4s', '5s', '6s', 
     '3x', '4x', 'fh', 
     'ss', 'ls', 
     'gm', 'ch'],
    ["1s", "2s", "3s", "4s", "5s", "6s", 
    '3 of a Kind', '4 of a Kind', 'Full House', 
    'Small Straight', 'Large Straight', 
    'GAMER', 'Chance'],
    ['', '', '', '', '', '',
     'Sum all dice', 'Sum all dice', '25 pts.', 
     '30 pts.', '40 pts.',
     '50 pts.', 'Sum all dice'],]




#############  MODES  ################


modes = ["rounds", "dice", 'puzzle']


mode_key = {"rounds": "R", "dice": "D", "puzzle": "P"}


# [0:mode_name, 1:description_short, 2:description_long, 3:description_img, 
#  4:icon white, 5:icon, 6:giphy]

modes_info = [
    ["rounds", 
        
        "Play round-based games within your group.", 
        
        "Rounds includes all round-based games such as board or card games,\
        sports or party games.\n\n \
        Each round you can enter points for every player. \
        The winner is the player with the most points.\n \
        This mode works for most types of games. Either you note down rounds\
        (as in scrabble) or \
        the results of multiple games you want to combine, e.g. cards or table tennis.\n\n \
        You will be able to anayze each game title seperately, \
        e.g. checking out who won most scrabble matches \
        or what is your win rate in table tennis.",
        
        "../static/media/modes/desc_mode.png", 
        "../static/media/modes/rounds_icon_tr.png", 
        "../static/media/modes/rounds_icon.png", 
        "https://giphy.com/embed/3tEFVAbfzzcwo",
    ],
    
    ["dice",
     
        "Roll 5 dice to gain points for specific combinations.",

        "You might know this game as 'Yatzy' or 'Kniffel' - this is it.\n \
        Players roll 5 dice to receive points in the given 13 categories. \
        The categories are pre-defined, examples are 'Multiple 3's' or 'Full House'. \
        The winner is the player with most points in total. \n\n \
        Don't worry if you don't know the rules, \
        Gamesbook will help you play it with ease.",

        "../static/media/modes/gamesbook_ref_d01.png",  
        "../static/media/modes/dice_icon_tr.png", 
        "../static/media/modes/dice_icon.png", 
        'https://giphy.com/embed/l2JdUMnCDg6qs368g',
    ],
    
    ["puzzle",
     
        "Save all puzzles you've finished and compare times.",

        "🧩 Challenge your (Jigsaw) puzzle skills!\n\n \
        Add all your puzzles to the Gamesbook library and \
        log the time it took you to finish them. \n \
        You can then log your times in GamesBook in a easy way. \
        Just add the puzzle once and then save logs each time you finish it. \n\n \
        After a view entries you will be able to explore your stats  \
        and compare within your group or between different puzzles.",

        "../static/media/modes/desc_mode.png", 
        "../static/media/modes/puzzle_icon_tr.png",
        "../static/media/modes/puzzle_icon.png",
        'https://giphy.com/embed/3o6Mbr1blVD5KKQBxK',
    ],
]      


mode_images = [
    ["../static/media/modes/gamesbook_ref_r07.png",
    "../static/media/modes/gamesbook_ref_r08.png",
    "../static/media/modes/gamesbook_ref_r09.png",
    "../static/media/modes/gamesbook_ref_r10.png",
    "../static/media/modes/gamesbook_ref_r11.png",
    "../static/media/modes/gamesbook_ref_r12.png"],
    ["../static/media/modes/gamesbook_ref_d01.png",
    "../static/media/modes/gamesbook_ref_d02.png",
    "../static/media/modes/gamesbook_ref_d03.png",
    "../static/media/modes/gamesbook_ref_d04.png",
    "../static/media/modes/gamesbook_ref_d06.png",
    "../static/media/modes/gamesbook_ref_d05.png"],
    ["../static/media/modes/gamesbook_ref_p01.png",
    "../static/media/modes/gamesbook_ref_p02.png",
    "../static/media/modes/gamesbook_ref_p03.png",
    "../static/media/modes/gamesbook_ref_p04.png",
    "../static/media/modes/gamesbook_ref_p05.png"],
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