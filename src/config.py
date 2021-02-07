import logging
import os
from logging import config

TOKEN = os.getenv('TOKEN')
BASE_URL = 'http://api.github.com'
CONTRIBUTORS_LENGTH = 30  # How many top contributors to show
OLD_PR_DAYS = 30  # PR considered old if it's open for more than this days
OLD_ISSUE_DAYS = 14  # Issue considered old if it's open for more than this days

LOGGING = {
    'version': 1,
    'formatters': {
        'console': {
            'format': '%(asctime)s - %(levelname)-8s %(name)-12s'
                      ' %(module)s:%(lineno)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

logging.config.dictConfig(LOGGING)
