def update_nba_game_results(season):
    import pandas as pd
    import regex as re
    import time
    from alive_progress import alive_bar
    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    from get_nba_game_results import get_nba_game_results
    
    gameResults = get_nba_game_results(season)
    
    gameResultsOld = pd.read_csv(r'C:\python\fs\nba\nba_game_results.csv')
    gameMerge = gameResults.merge(gameResultsOld, on='gameID', how='left', indicator=True)
    gameList = gameMerge.loc[gameMerge['_merge']=='left_only', 'gameID']
    gameResultsNew = gameResults[gameResults['gameID'].isin(gameList)]
    
    newGameID = gameResultsNew['gameID'].values.tolist()
    referees = []
    
    with alive_bar(len(newGameID), title='# of games scores collected') as bar1:
        for gameID in newGameID:
            brLink = r'https://www.basketball-reference.com/boxscores/{}.html'.format(gameID)
            html = urlopen(brLink)
            soup = BeautifulSoup(html, features='lxml')
            referees_soup = soup.find_all('a', href=re.compile(r'referees'))
            referees_list = [referee.string for referee in referees_soup]
            referees_list = referees_list[:referees_list.index('Referees')]
            referees.append(referees_list)
            time.sleep(3)
            bar1()
    
    gameResultsNew['referees'] = referees
    
    gameResultsNew.to_csv(r'C:\python\fs\nba\nba_game_results.csv', mode='a', index=False, header=False)
    
    return newGameID