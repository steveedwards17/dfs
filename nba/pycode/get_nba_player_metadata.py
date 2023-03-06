# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 21:05:59 2022

@author: steph
"""

def get_nba_player_metadata(link):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime as dt
    
    urlRoot = 'https://www.basketball-reference.com'
    url = urlRoot + link
    
    html = urlopen(url)
    players_page = BeautifulSoup(html, features='lxml')
    
    body = players_page.find('body').text
    body = body[body.find('Twitter:'):]
    body = body[:body.find('Experience:')]
    body = body.split('\n')
    collegeBool = True in ['College:' in row for row in body]
    draftBool = True in ['Draft:' in row for row in body]
    twitterBool = True in ['Twitter:' in row for row in body]
    instagramBool = True in ['Instagram:' in row for row in body]
    
    if len(body) == 1:
        body = players_page.find('body').text
        body = body[body.find('Instagram:'):]
        body = body[:body.find('Experience:')]
        body = body.split('\n')
        collegeBool = True in ['College:' in row for row in body]
        draftBool = True in ['Draft:' in row for row in body]
        twitterBool = True in ['Twitter:' in row for row in body]
        instagramBool = True in ['Instagram:' in row for row in body]
        if len(body) != 1:
            body.insert(0, 'Twitter:')
            body.insert(1, 'N/A')
            if not instagramBool:
                body.insert(2, 'Instagram:')
                body.insert(3, 'N/A')
              
    if len(body) == 1:
        body = players_page.find('body').text
        body = body[body.find('Position:'):]
        body = body[:body.find('Experience:')]
        body = body.split('\n')
        collegeBool = True in ['College:' in row for row in body]
        draftBool = True in ['Draft:' in row for row in body]
        twitterBool = False
        instagramBool = False
        body.insert(0, 'Twitter:')
        body.insert(1, 'N/A')
            
    if not instagramBool:
        body.insert(2, 'Instagram:')
        body.insert(3, 'N/A')

    bodyText = []
    for row in body:
        row = row.replace('\n','')
        row = row.replace('\xa0','')
        row = row.strip()
        if len(row) > 1:
            bodyText.append(row)

    data = {}
    
    for value in bodyText:
        try:
            if twitter == 'ready':
                data['twitter'] = value
                twitter = 'done'
            if instagram == 'ready':
                data['instagram'] = value
                instagram = 'done'
            if position == 'ready':
                data['position'] = value
                position = 'done'
            if shoots == 'ready':
                data['shoots'] = value
                shoots = 'done_'
            if heightWeight == 'ready':
                data['heightWeight'] = value
                heightWeight = 'done'
            if birthDay == 'ready':
                data['birthDay'] = value[:-1]
                birthDay = 'done_'
            if birthYear == 'ready':
                data['birthYear'] = value
                birthYear = 'done'
            if country == 'ready':
                data['homeCountry'] = value.upper()
                country = 'done'
            
            if collegeBool:
                if college == 'ready':
                    data['college'] = value
                    college = 'done'
            
            if draft == 'ready':
                data['draft'] = value
                draft = 'done'
        except:
            pass

        if 'Twitter:' in value:
            twitter = 'ready'
        if 'Instagram:' in value:
            instagram = 'ready'
        if 'Position:' in value:
            position = 'ready'
        if 'Shoots:' in value:
            shoots = 'ready'
        try:
            if shoots == 'done_':
                heightWeight = 'ready'
                shoots = 'done'
        except:
            pass
        if 'Born:' in value:
            birthDay = 'ready'
        try:
            if birthDay == 'done_':
                birthYear = 'ready'
                birthDay = 'done'
        except:
            pass
        if value.startswith('in'):
            data['hometown'] = value[2:]
            country = 'ready'
        if value.startswith('Relatives:'):
            data['relatives'] = value.split()[-1]
        
        if collegeBool:
            if 'College:' in value:
                college = 'ready'
        
        if 'Draft:' in value:
            draft = 'ready'
        if value.startswith('NBA Debut:'):
            data['nbaDebut'] = value.replace('NBA Debut:','')
    data['link'] = link
    df = pd.DataFrame(data, index=[0])
    df['homeState'] = df['hometown'].apply(lambda x: x.split(',')[-1])
    df['homeTown'] = df['hometown'].apply(lambda x: x.split(',')[0])
    df['heightMetric'] = df['heightWeight'].apply(lambda st: st[st.find('(')+1:st.find(')')])
    df['weightMetric'] = df['heightMetric'].apply(lambda x: x.split(',')[-1])
    df['heightMetric'] = df['heightMetric'].apply(lambda x: x.split(',')[0])
    df['height'] = df['heightWeight'].apply(lambda x: x.split('(')[0])
    df['weight'] = df['height'].apply(lambda x: x.split(',')[-1])
    df['height'] = df['height'].apply(lambda x: x.split(',')[0])
    df.drop('heightWeight', inplace=True, axis=1)
    df['position'] = df['position'].str.replace('Point Guard', 'PG'
                                               ).str.replace('Shooting Guard', 'SG'
                                                            ).str.replace('Small Forward', 'SF'
                                                                         ).str.replace('Power Forward', 'PF'
                                                                                      ).str.replace('Center', 'C').str.replace('and',''
                                                                                                                              ).str.replace(',','')
    
    if draftBool == True:
        df['nbaDraftTeam'] = df['draft'].apply(lambda x: x.split(',')[0])
        df['nbaDraftRound'] = df['draft'].apply(lambda x: x.split(',')[1]).str.replace('(','')
        df['nbaDraftPick'] = df['draft'].apply(lambda x: x.split(',')[2]).str.replace(')','')
        df.drop('draft', inplace=True, axis=1)
    else:
        df['nbaDraftTeam'] = ''
        df['nbaDraftRound'] = ''
        df['nbaDraftPick'] = ''
    df['birthDay'] = df['birthDay'] + ', ' + df['birthYear']
    df.drop('birthYear', inplace=True, axis=1)
    
    if 'relatives' in df:
        df['nbaLegacy'] = 'Y'
    else:
        df['nbaLegacy'] = 'N'
        df['relatives'] = ''
    
    if 'college' not in df:
        df['college'] = ''
        
    df['updateDate'] = pd.Timestamp.now().strftime("%Y-%m-%d")
        
    df = df[['position','shoots','height','heightMetric','weight','weightMetric','college','homeTown','homeState','homeCountry','birthDay','nbaDebut','nbaDraftRound','nbaDraftPick','nbaDraftTeam','nbaLegacy','relatives','twitter','instagram','link','updateDate']]
    
    data = {}
    
    return df