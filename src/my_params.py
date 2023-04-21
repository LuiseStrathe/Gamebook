
modes = ["rounds", "dice", 'puzzle', 'skat']
mode_key = {"rounds": "R", "dice": "D", "puzzle": "P", "skat": "S"}

mode_giphs = ["https://giphy.com/embed/3tEFVAbfzzcwo", 'https://giphy.com/embed/l2JdUMnCDg6qs368g', 
              'https://giphy.com/embed/3o6Mbr1blVD5KKQBxK', 'https://giphy.com/embed/3o7btPCcdNniyf0ArS']
              

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
                Play with your 24 cards set and 3 to 4 players.\n \
                After each round, the winners ponts will be updated."]


about_info = str(' '.join([
    "This GameBook functions a simple and free online game notebook, as you might have one at home.\n\n",
    "It is a simple web application that allows you to create and manage your gameplay in the analog world.", 
    "This is for 2 to 8 players per group, competing against each other.",
    "Each game you play will add a page to your GameBook with the final results.",
    "With your group GameBook you have access to statistics of all your group's games."]))

result_cols = ['game_id', 'mode', "group",
               "result", "n_rounds", "winner", 'info', 'time']

player_cols = ['name', 'info', 'tag', 'image']

path_data = 'data/'


