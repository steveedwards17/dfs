def run_nfl_refresh(week):
    from update_nfl_game_results import update_nfl_game_results
    from get_nfl_boxscore import get_nfl_boxscore
    
    season = '2021'
    
    newGameID = update_nfl_game_results(week, season)
    print('{} new NFL game results from week {} have been added to nfl_game_results.csv'.format(len(newGameID), week))
    
    for gameID in newGameID:
        get_nfl_boxscore(gameID)