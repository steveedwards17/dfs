def get_nfl_boxscore(gameID):
    import pandas as pd
    
    brLink = r'https://www.pro-football-reference.com/boxscores/{}.htm'.format(gameID)
    boxscores = pd.read_html(brLink)
    
    gameResults = pd.read_csv(r'C:\python\fs\nfl\nfl_game_results.csv')
    overtime = gameResults[gameResults['gameID'] == gameID]['overtimeInd'].values[0]
    
    boxscoreList = boxscores[0].values.tolist()
    if overtime == 'OT':
        boxscoreList = [gameID, boxscoreList[0][2], boxscoreList[0][3], boxscoreList[0][4], boxscoreList[0][5], boxscoreList[0][6], boxscoreList[1][2], boxscoreList[1][3], boxscoreList[1][4], boxscoreList[1][5], boxscoreList[1][6]]
    else:
        boxscoreList = [gameID, boxscoreList[0][2], boxscoreList[0][3], boxscoreList[0][4], boxscoreList[0][5], 0, boxscoreList[1][2], boxscoreList[1][3], boxscoreList[1][4], boxscoreList[1][5], 0]
    quarterByQuarterbox = pd.DataFrame(boxscoreList).T
    columnNames = ['gameID','visitorQ1','visitorQ2','visitorQ3','visitorQ4','visitorOT','homeQ1','homeQ2','homeQ3','homeQ4','homeOT']
    quarterByQuarterbox.columns = columnNames
    quarterByQuarterbox = quarterByQuarterbox[quarterByQuarterbox['gameID'] != 'gameID']
    quarterByQuarterbox.to_csv(r'C:\python\fs\nfl\nfl_quarter_by_quarter.csv', mode='a', index=False, header=False)
    
    scoringDetail = boxscores[1]
    columnNames = ['quarter','time','team','detail','visitorScore','homeScore']
    scoringDetail.columns = columnNames
    scoringDetail.fillna(method='ffill', inplace=True)
    scoringDetail['gameID'] = gameID
    scoringDetail = scoringDetail[scoringDetail['team'] != 'team']
    scoringDetail.to_csv(r'C:\python\fs\nfl\nfl_scoring_detail.csv', mode='a', index=False, header=False)
    
    offenseBoxscore = boxscores[2]
    columnNames = ['player','team','passComp','passAtt','passYds','passTD','passInt','timesSacked','sackYds','passLng','passRate','rushAtt','rushYds','rushTD','rushLng','recTgt','recRec','recYds','recTD','recLng','fmb','fl']
    offenseBoxscore.columns = columnNames
    offenseBoxscore.drop(offenseBoxscore[(offenseBoxscore.player.isna()) | (offenseBoxscore.player == 'Player')].index, inplace=True)
    offenseBoxscore['gameID'] = gameID
    
    gameResults = pd.read_csv(r'C:\python\fs\nfl\nfl_game_results.csv')
    offenseBoxscore = offenseBoxscore.merge(gameResults, how='left', on='gameID')
    offenseBoxscore['homeInd'] = offenseBoxscore.apply(lambda x: 'Y' if x['team'] == x['homeTeamAbbrev'] else 'N', axis=1)
    offenseBoxscore['opponent'] = offenseBoxscore.apply(lambda x: x['visitingTeamAbbrev'] if x['homeInd'] == 'Y' else x['homeTeamAbbrev'], axis=1)
    #gameResults.drop(columns=['team_x','team_y'], inplace=True)
    #gameResults.rename(columns={'teamAbbrev_x':'visitingTeamAbbrev','teamAbbrev_y':'homeTeamAbbrev'}, inplace=True)
    
    offenseBoxscore.to_csv(r'C:\python\fs\nfl\nfl_offense_boxscore.csv', mode='a', index=False, header=False)