
modes = ["rounds", "dice", 'puzzle', 'skat']


mode_key = {"rounds": "R", "dice": "D", "puzzle": "P", "skat": "S"}



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
       
                
mode_giphs = ["https://giphy.com/embed/3tEFVAbfzzcwo", 'https://giphy.com/embed/l2JdUMnCDg6qs368g', 
              'https://giphy.com/embed/3o6Mbr1blVD5KKQBxK', 'https://giphy.com/embed/3o7btPCcdNniyf0ArS']
              
            
puzzle_cols = ['id', 'title', 'description', 'pcs']


dice_rows = ["1's", "2's", "3's", "4's", "5's", "6's", '3 of a kind',
                '4 of a kind', 'full house', 'small straight', 'large straight', 'YEAHA', 'chance']



path_data = 'data/'


page_titles = {
    "_about.html": "About GamesBook",
    "_index.html": "Home",
    "dice_page.html": "Dice Game",
    "dice_start.html": "Dice Game",
    "dice.html": "Dice Game",
    "gamebook.html": "Overview",
    "group_register.html": "Register",
    "group_login.html": "Login",
    "group_settings.html": "Settings",
    "group.html": "Overview",
    "puzzle_list.html": "Puzzles",
    "puzzle_record.html": "Puzzle Records",
    "puzzle_stats.html": "Puzzle Stats",
    "random.html": "Test GamesBook",
    "rounds_page.html": "Rounds",
    "rounds.html": "Rounds",
}



descriptions = ["Play in rounds with your group.\n\n \
                In each round, you can enter points for each player.\n \
                The winner is the player with the most points over all rounds.\n\n \
                You can use this mode for all kinds of games. Either you note down rounds \
                (as in scrabble) or \
                the results of multiple games you want to combine, e.g. cards or table tennis.",
                
                "Roll the dice and as in the classic achieve points in different categories. \n\n \
                You need 5 Dice. The acitve player can reroll with twice.\n \
                Each time you roll the dice, you can choose which dice you want to keep. \
                You can not reroll with those anymore.\n \
                To end your turn you have to choose a combination and enter the points.\n \
                The winner is the player with the most total points.",
                
                "Time your puzzle skills\n\n \
                You can enter your puzzle times in the GameBook.\n \
                For this you can specify the puzzle and the time.\n \
                Also you can save puzzles and later see how group members performed.",
                
                "Note down your skat results\n\n \
                Play with your 32 cards set and 3 to 4 players.\n \
                After each round, the winners ponts will be updated."]


about_info = str(' '.join([
    "This GameBook functions a simple and free online game notebook, as you might have one at home.\n\n",
    "It is a simple web application that allows you to create and manage your gameplay in the analog world.", 
    "This is for 2 to 8 players per group, competing against each other.",
    "Each game you play will add a page to your GameBook with the final results.",
    "With your group GameBook you have access to statistics of all your group's games."]))

                
    