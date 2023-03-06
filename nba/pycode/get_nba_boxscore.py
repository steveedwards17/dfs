def get_nba_boxscore(gameID):
    import pandas as pd
    import regex as re
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    
    brLink = r'https://www.basketball-reference.com/boxscores/{}.html'.format(gameID)
    boxscores = pd.read_html(brLink)
    
    html = urlopen(brLink)
    stats_page = BeautifulSoup(html, features='lxml')
    playersSoup = stats_page.find_all('a', href=re.compile(r'/players/'))
    playersList = [(player.contents, player['href']) for player in playersSoup]
    playersDf = pd.DataFrame(playersList, columns=['Starters','playerLink'])
    playersDf.update(playersDf.Starters.str[0])
    playersDf.drop(playersDf.index[playersDf['Starters'] == 'Players'], inplace = True)
    playersDf.drop(playersDf.index[playersDf['playerLink'] == '/players/'], inplace = True)
    playersDf = playersDf[playersDf['Starters'].str.len() > 0]
    playersDf.drop_duplicates(inplace=True, ignore_index=True)
    
    gameResults = pd.read_csv(r'C:\python\fs\nba\nba_game_results.csv')
    overtime = gameResults[gameResults['gameID'] == gameID]['overtimeInd'].values[0]
    
    statType = ['Game','Q1','Q2','H1','Q3','Q4','H2','Advanced']
    if overtime == 'OT':
        statType.insert(7, 'OT1')
    if overtime == '2OT':
        statType[7:7] = ['OT1','OT2']
    if overtime == '3OT':
        statType[7:7] = ['OT1','OT2','OT3']
        
    numOfBoxscores = len(statType)
    homeAway = (['Away'] * numOfBoxscores) + (['Home'] * numOfBoxscores)
    statType = statType * 2
    
    for idx, boxscore in enumerate(boxscores):        
        columns = []
        fixColumns = boxscore.columns
        for column_tup in fixColumns:
            columns.append(column_tup[1])
        boxscore.columns = columns
        
        boxscore['stat'] = statType[idx]
        boxscore['team'] = homeAway[idx]
        boxscore['gameID'] = gameID
        
        teamTotals = boxscore[(boxscore['Starters'] == 'Team Totals') & (boxscore['stat'] != 'Advanced')]
        teamTotals.drop('Starters', axis=1, inplace=True, errors='ignore')
        teamTotals.drop('+/-', axis=1, inplace=True, errors='ignore')
        teamTotals.to_csv(r'C:\python\fs\nba\nba_team_game_totals.txt', mode='a', index=False, header=False)
        boxscore.drop(boxscore[boxscore.Starters == 'Team Totals'].index, inplace=True)
        
        units = (['Starter'] * 5) + (['Reserve'] * (boxscore.shape[0] - 5))
        boxscore['Unit'] = units
        
        boxscore = pd.merge(boxscore, playersDf, on='Starters', how='left')
        
        boxscore.fillna(0, inplace=True)
        boxscore.drop(boxscore[boxscore.Starters == 'Reserves'].index, inplace=True)
        boxscore.drop(boxscore[boxscore.MP == 'Did Not Play'].index, inplace=True)
        boxscore.drop(boxscore[boxscore.MP == 'Did Not Dress'].index, inplace=True)
        boxscore.drop(boxscore[boxscore.MP == 'Not With Team'].index, inplace=True)
        boxscore.drop(boxscore[boxscore.MP == 'Player Suspended'].index, inplace=True)
        
        if statType[idx] == 'Advanced':
            boxscore.to_csv(r'C:\python\fs\nba\nba_advanced_boxscore.txt', mode='a', index=False, header=False)
        else:
            boxscore.to_csv(r'C:\python\fs\nba\nba_basic_boxscore.txt', mode='a', index=False, header=False)
