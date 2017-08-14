"""
@created_at 2017-08-12
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

import os


root_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

DATA_PATH = os.path.join(root_path, 'tests', 'data')
os.makedirs(DATA_PATH, exist_ok=True)

LOGLEVEL = 'DEBUG'
