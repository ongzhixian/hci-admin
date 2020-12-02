################################################################################
# Modules and functions import statements
################################################################################

import logging
from helpers.app_runtime import app
from modules import *
from api import *
from pages import *
from os import getenv

################################################################################
# Set logging levels
################################################################################

if getenv('GAE_ENV', '').startswith('standard'):
    # Setup for logging in AppEngine environments
    logging.getLogger().setLevel(logging.DEBUG)
else:
    # Setup for logging in non-AppEngine environments
    # logging_format = logging.Formatter('%(asctime)-15s %(levelname)-8s %(name)-5s %(message)s')
    logging_format = logging.Formatter('%(asctime)-15s %(levelname)-8s %(funcName)-20s %(message)s')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    default_console_logger = root_logger.handlers[0]
    default_console_logger.setFormatter(logging_format)

    # Uncomment to log to file (Comment out for GCP)
    file_logger = logging.FileHandler('hci-admin-app-engine.log')
    file_logger.setFormatter(logging_format)
    root_logger.addHandler(file_logger)


################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    # Note: This is used when running locally only. 
    # When deploying to Google App Engine, a webserver process such as Gunicorn will serve the app. 
    # This can be configured by adding an `entrypoint` to app.yaml (to run under uwsgi).

    # Flask's development server will automatically serve static files in the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files.
    # Once deployed, App Engine itself will serve those files as configured in app.yaml.
    # from modules import app_version
    # app_version.incr_revision()
    from datetime import datetime
    logging.info("[PROGRAM START]")
    logging.critical("%8s test message %s" % ("CRITICAL", str(datetime.utcnow())))
    logging.error("%8s test message %s" % ("ERROR", str(datetime.utcnow())))
    logging.warning("%8s test message %s" % ("WARNING", str(datetime.utcnow())))
    logging.info("%8s test message %s" % ("INFO", str(datetime.utcnow())))
    logging.debug("%8s test message %s" % ("DEBUG", str(datetime.utcnow())))
    app.run(host='127.0.0.1', port=8080, debug=True)
