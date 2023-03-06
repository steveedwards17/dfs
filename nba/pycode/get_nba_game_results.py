def get_nba_game_results(season):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import pandas as pd
    import calendar
    import time
    
    months = calendar.month_name[1:]
    
    gameResults = pd.DataFrame(columns=['date','startTime','visitingTeam','visitingPoints','homeTeam','homePoints','overtimeInd','attendance','arenaName','gameID','season','referees'])
    
    for month in months:
    
        url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html'.format(season, month.lower())
        try:
            html = urlopen(url)
        except:
            continue
        
        stats_page = BeautifulSoup(html, features='lxml')
        tbl = stats_page.find('table')
        rows = tbl.findAll('tr')
        
        gameIDs = []
        for row in rows:
            cols = row.find_all('th')
            for col in cols:
                if col.has_attr('csk'):
                    gameIDs.append(col.get('csk'))

        gameResultsStg = pd.read_html(url)[0]

        colsToDrop = [6,10]
        gameResultsStg.drop(gameResultsStg.columns[colsToDrop], axis=1, inplace=True)
    
        columnNames = ['date','startTime','visitingTeam','visitingPoints','homeTeam','homePoints','overtimeInd','attendance','arenaName']
        gameResultsStg.columns = columnNames
    
        gameResultsStg['date'] = pd.to_datetime(gameResultsStg['date'], format='%a, %b %d, %Y')
        gameResultsStg['startTime'] = gameResultsStg['startTime'].str[:] + 'm'
        gameResultsStg['overtimeInd'].fillna('N', inplace=True)
        gameResultsStg['attendance'].fillna(0, inplace=True)
        gameResultsStg['attendance'] = gameResultsStg['attendance'].astype('int')
        gameResultsStg['gameID'] = gameIDs
        gameResultsStg['season'] = season
        gameResultsStg['referees'] = ''
        
        gameResults = pd.concat([gameResults, gameResultsStg])
        gameResults.dropna(subset=['visitingPoints','homePoints'], inplace=True)
        
        time.sleep(3)

    return gameResults