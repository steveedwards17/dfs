def update_nfl_game_results(week, season):
    import pandas as pd
    from get_nfl_game_results import get_nfl_game_results
    
    gameResults = get_nfl_game_results(week, season)
    
    gameResultsOld = pd.read_csv(r'C:\python\fs\nfl\nfl_game_results.csv')
    gameMerge = gameResults.merge(gameResultsOld, on='gameID', how='left', indicator=True)
    gameList = gameMerge.loc[gameMerge['_merge']=='left_only', 'gameID']
    gameResultsNew = gameResults[gameResults['gameID'].isin(gameList)]
    gameResultsNew.to_csv(r'C:\python\fs\nfl\nfl_game_results.csv', mode='a', index=False, header=False)
    
    newGameID = gameResultsNew['gameID'].values.tolist()
    
    return newGameID