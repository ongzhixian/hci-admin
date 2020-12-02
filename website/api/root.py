# 
################################################################################
# Modules and functions import statements
################################################################################

import json
import logging

from datetime import datetime
from time import time

from flask import request, make_response, abort

from helpers.app_runtime import app

from modules.security import make_keys

################################################################################
# Setup routes
# /api/datetime     -- Get server UTC datetime
# /api/epochtime    -- Get server epoch time 
# /api/test         -- Function to 
################################################################################

@app.route('/api/datetime', methods=['GET', 'POST'])
def api_datetime(errorMessages=None):

    logging.info("In api_datetime()")

    return str(datetime.utcnow())


@app.route('/api/epochtime', methods=['GET', 'POST'])
def api_epochtime(errorMessages=None):

    logging.info("In api_epochtime()")

    return str(int(time()))


@app.route('/api/echo', methods=['GET'])
def api_echo(errorMessages=None):

    logging.info("In api_echo()")

    if "msg" in request.args:
        return "re:{0}".format(request.args["msg"])
    abort(400)

@app.route('/api/make_keys', methods=['GET'])
def api_make_keys(errorMessages=None):

    logging.info("In api_make_keys()")

    keys = make_keys("aes", 32, 16)

    return json.dumps(keys)