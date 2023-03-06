def get_nfl_game_results(week, season):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import pandas as pd
    import re
    
    url = 'https://www.pro-football-reference.com/years/{}/week_{}.htm'.format(season, str(week))
    html = urlopen(url)
    stats_page = BeautifulSoup(html, features='lxml')
    rows = stats_page.findAll('a')
    gameIDs = []
    
    for row in rows:
        if re.match(r'/boxscores/\d', row['href']):
            gameIDs.append(re.sub('/boxscores/|.htm', '', row['href']))
    
    gameResults = pd.read_html(url)
    
    dfs = []
    for idx, df in enumerate(gameResults):
        if (idx % 2) == 0 and idx <= (len(gameIDs) * 2) - 2:
            gameResultList = df.T.values.tolist()
            gameResultList = [gameResultList[0][0], gameResultList[0][1], gameResultList[0][2], gameResultList[1][1], gameResultList[1][2], gameResultList[2][2]]
            gameResult = pd.DataFrame(gameResultList).T
            dfs.append(gameResult)
    gameResults = pd.concat(dfs)
    columnNames = ['date','visitingTeam','homeTeam','visitingPoints','homePoints','overtimeInd']
    gameResults.columns = columnNames
    gameResults.reset_index(inplace=True, drop=True)
    gameResults['date'] = pd.to_datetime(gameResults['date'], format='%b %d, %Y')
    gameResults['overtimeInd'].fillna('N', inplace=True)
    gameResults['gameID'] = gameIDs
    gameResults['week'] = week
    
    nflTeamAbbrev = pd.read_csv(r'C:\python\fs\nfl\referenceFiles\NFLTeamAbbreviations.csv')
    gameResults = gameResults.merge(nflTeamAbbrev, how='left', left_on='visitingTeam', right_on='team')
    gameResults = gameResults.merge(nflTeamAbbrev, how='left', left_on='homeTeam', right_on='team')
    gameResults.drop(columns=['team_x','team_y'], inplace=True)
    gameResults.rename(columns={'teamAbbrev_x':'visitingTeamAbbrev','teamAbbrev_y':'homeTeamAbbrev'}, inplace=True)
            
    return gameResults