# ako.py
################################################################################
# Modules and functions import statements
################################################################################

import logging
from helpers.app_runtime import app
from modules import *
# from api import *
# from pages import *
from datetime import datetime

################################################################################
# Set logging levels
################################################################################

logging_format = logging.Formatter('%(asctime)-15s %(levelname)-8s %(name)-5s %(message)s')
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
default_console_logger = root_logger.handlers[0]
default_console_logger.setFormatter(logging_format)

# Uncomment to log to file (Comment out for GCP)
file_logger = logging.FileHandler('logs/dev.log')
file_logger.setFormatter(logging_format)
root_logger.addHandler(file_logger)


################################################################################
# Main function
################################################################################

def print_test_logs():
    logging.critical("%8s test message %s" % ("CRITICAL", str(datetime.utcnow())))
    logging.error("%8s test message %s" % ("ERROR", str(datetime.utcnow())))
    logging.warning("%8s test message %s" % ("WARNING", str(datetime.utcnow())))
    logging.info("%8s test message %s" % ("INFO", str(datetime.utcnow())))
    logging.debug("%8s test message %s" % ("DEBUG", str(datetime.utcnow())))

if __name__ == '__main__':
    logging.info("[PROGRAM START]")
    # print_test_logs()


    logging.info("[PROGRAM END]")