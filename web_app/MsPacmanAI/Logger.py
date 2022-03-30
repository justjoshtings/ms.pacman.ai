"""
Logger.py

Add logging object for logging.

author: @justjoshtings
created: 3/20/2022
"""
import logging
import logging.handlers
from datetime import datetime

class MyLogger:
    '''
    Add logging object for logging.
    '''
    def __init__(self, log_filename):
        '''
        Params:
            self: instance of object
            log_filename (str): path to logging file name
        '''
        # Set up a specific logger with our desired output level
        self.my_logger = logging.getLogger('my_logger')
        self.my_logger.setLevel(logging.DEBUG)
        
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
                    log_filename, maxBytes=10000000, backupCount=2)

        self.my_logger.addHandler(handler)
    
    def get_mylogger(self):
        '''
        Get logger object

        Params:
            self: instance of object
        
        Return:
            self.my_logger (logger object): returns the logger object
        '''
        return self.my_logger

    def goodbye(self):
        '''
        Last log before exiting program

        Params:
            self: instance of object
        '''
        self.my_logger.info(f'{datetime.now()} -- Exiting program...')