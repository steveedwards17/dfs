# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 21:12:28 2022

@author: steph
"""

def update_nba_player_metadata():
    import pandas as pd
    import time
    from alive_progress import alive_bar
    from get_nba_player_metadata import get_nba_player_metadata
    
    allPlayers = pd.read_csv(r'C:\python\fs\nba\nba_basic_boxscore.txt')[['playerLink']].drop_duplicates()
    
    playerDataOld = pd.read_csv(r'C:\python\fs\nba\nba_player_metadata.txt')
    playerMerge = allPlayers.merge(playerDataOld, left_on='playerLink', right_on='link', how='left', indicator=True)
    playerList = playerMerge.loc[playerMerge['_merge']=='left_only', 'playerLink']
    playerDataNew = allPlayers[allPlayers['playerLink'].isin(playerList)]
    
    newPlayer = playerDataNew['playerLink'].values.tolist()
    
    with alive_bar(len(newPlayer), title='# of player metadata collected') as bar3:
        df = None
        for player in newPlayer:
            try:
                if df == None:
                    df = get_nba_player_metadata(player)
                else:
                    df = pd.concat([df, get_nba_player_metadata(player)])
            except:
                with open(r'C:\python\fs\nba\nba_player_metadata_fallout.txt', 'a') as f:
                    f.write(player + '\n')
            time.sleep(3)
            bar3()
    
    
    if len(df) > 0:
        df.to_csv(r'C:\python\fs\nba\nba_player_metadata.txt', mode='a', index=False, header=False)
        
    
    return newPlayer