# -*- coding: utf-8 -*-
'''Log module for applications
'''
import sys
import logging
from logging import debug, info, warning, error, critical
from os.path import basename, abspath, join


log_dir = join(basename(abspath(__file__)), 'log')
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(module)s.%(funcName)s - %(message)s'
LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S %z'
LOG_LEVEL = logging.WARNING


def get_opts():
    '''Get options from sys.argv, return a tuple with options in fellow order

    Options:
        --loglevel=INFO|DEBUG|WARNING|ERROR|CRITICAL, int, logging level int
        --debug|_d, bool, it will set log level to debug
        --logfile=log file path, string
        --loghere|_h, bool, create log file in the directory of application
        --stderr|_e, print logs to consoler
    '''
    loglevel = None
    is_debug = False
    logfile = None
    loghere = False
    to_stderr = False
    for opt in sys.argv[1:]:
        if opt == '--debug' or opt == '_d':
            is_debug = True
        elif opt.startswith('--loglevel='):
            level_str = opt.replace('--loglevel=', '', 1)
            loglevel = getattr(logging, level_str.upper(), None)
            if not isinstance(loglevel, int):
                raise ValueError('Invalid log level: %s' % level_str)
        elif opt == '--loghere' or opt == '_h':
            loghere = True
        elif opt.startswith('--logfile='):
            logfile = opt.replace('--logfile=', '', 1)
        elif opt == '--stderr' or opt == '_e':
            to_stderr = True
    return (loglevel, is_debug, logfile, loghere, to_stderr)


app_name = basename(sys.argv[0])
log_file = '{0}/{1}.log'.format(log_dir, app_name)
logger = logging.getLogger()
# parse sys.argv options
user_log_level, user_is_debug, user_log_file, user_log_here, \
        user_to_stderr = get_opts()
# log level
if user_is_debug:
    LOG_LEVEL = logging.DEBUG
else:
    if user_log_level:
        LOG_LEVEL = user_log_level
logger.setLevel(LOG_LEVEL)
# handler
if user_to_stderr:
    handler = logging.StreamHandler()
else:
    if user_log_here:
        log_file = app_name + '.log'
    else:
        if user_log_file:
            log_file = user_log_file
    handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
# formatter
handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_TIME_FORMAT))
logger.addHandler(handler)

# Fake function, these functions are import from logging
# def debug(msg, ...): 
#   pass

# def info(msg, ...): 
#   pass

# def warning(msg, ...): 
#   pass

# def error(msg, ...): 
#   pass

# def critical(msg, ...): 
#   pass
