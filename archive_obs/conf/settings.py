"""
@created_at 2017-08-12
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

import importlib
import os
import sys


PROJECT_NAME = 'archive_obs'

TESTING = 'test' in sys.argv or 'test_coverage' in sys.argv
PYTHON_ENV = os.environ.get('PYTHON_ENV', 'dev')

if TESTING:
    PYTHON_ENV = 'test'

env_setting = importlib.import_module('{}.conf.{}_settings'.format(PROJECT_NAME, PYTHON_ENV))

ROOT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

DATA_PATH = env_setting.DATA_PATH or os.path.join(ROOT_PATH, 'data')
os.makedirs(DATA_PATH, exist_ok=True)
RAW_PATH = os.path.join(DATA_PATH, 'raw')
os.makedirs(RAW_PATH, exist_ok=True)
CSV_PATH = os.path.join(DATA_PATH, 'csv')
os.makedirs(CSV_PATH, exist_ok=True)

FITS_HEADER_EXTENSION = '.dat'

ENCODING_UTF8 = 'utf-8'

# =============================================================================
# Logging
# =============================================================================
LOG_DIR = os.environ.get('LOG_DIR') or os.path.join(ROOT_PATH, 'log')
LOGLEVEL = env_setting.LOGLEVEL or os.environ.get('LOGLEVEL', 'INFO')
os.makedirs(LOG_DIR, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'dev_friendly': {
            'format': '[%(levelname)7s] %(asctime)s  %(name)20s %(lineno)3d | %(message)s',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev_friendly',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'archive_obs.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'root': {
        'level': LOGLEVEL,
        'handlers': ['console', 'file'],
    },
}

# =============================================================================
# Archives URLs
# =============================================================================
SCRAPER_ARCHIVE_URLS = {
    'gemini': 'https://archive.gemini.edu/',
}
