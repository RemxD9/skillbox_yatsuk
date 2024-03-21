config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'sys.stdout',
            'filters': ['ascii_filter']
        },
        'info_file': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': 'calc_info.log',
            'filters': ['ascii_filter']
        },
        'utils_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': 'utils.log',
            'when': 'H',
            'interval': 10,
            'backupCount': 0,
            'encoding': 'utf-8',
            'filters': ['ascii_filter']
        }
    },
    'loggers': {
        '': {
            'handlers': ['info_file'],
            'level': 'INFO',
            'propagate': False
        },
        'utils': {
            'handlers': ['utils_file'],
            'level': 'INFO',
            'propagate': False
        }
    },
    'filters': {
        'ascii_filter': {
            '()': 'ASCIIFilter.ASCIIFilter'
        }
    },
}
