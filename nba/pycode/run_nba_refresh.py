def run_nba_refresh(season):
    from alive_progress import alive_bar
    from update_nba_game_results import update_nba_game_results
    from update_nba_player_metadata import update_nba_player_metadata
    from get_nba_boxscore import get_nba_boxscore
    import time
    
    newGameID = update_nba_game_results(season)
    
    with alive_bar(len(newGameID), title='# of boxscores collected') as bar2:
        for gameID in newGameID:
            get_nba_boxscore(gameID)
            time.sleep(5)
            bar2()
            
    update_nba_player_metadata()