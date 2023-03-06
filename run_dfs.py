import sys
import warnings

# warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

sys.path.insert(0, r'C:/python/fs/nba/pycode/')
sys.path.insert(0, r'C:\Users\steph\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages')

import run_nba_refresh

# https://swishanalytics.com/nba/

season = '2023'

run_nba_refresh.run_nba_refresh(season)