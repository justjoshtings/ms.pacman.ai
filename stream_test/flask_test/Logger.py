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
    def __init__(self, log_filename):
        # Set up a specific logger with our desired output level
        self.my_logger = logging.getLogger('my_logger')
        self.my_logger.setLevel(logging.DEBUG)
        
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
                    log_filename, maxBytes=10000000, backupCount=2)

        self.my_logger.addHandler(handler)
    
    def get_mylogger(self):
        return self.my_logger

    def goodbye(self):
        self.my_logger.info(f'{datetime.now()} -- Exiting program...')