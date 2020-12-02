# 
################################################################################
# Modules and functions import statements
################################################################################

import logging
from helpers.app_runtime import app
from helpers.app_helper import view, get_model

# from modules.message import add_message

################################################################################
# Setup routes
################################################################################

@app.route('/api/message', methods=['GET', 'POST'])
def api_message(errorMessages=None):

    logging.info("In api_message()")

    # add_message("hello world 2")

    return "OK"
    #return str(datetime.utcnow())


@app.route('/api/msg', methods=['GET', 'POST'])
def api_msg(errorMessages=None):

    logging.info("In api_msg()")

    # add_message("hello world 2")

    return "OK"
    #return str(datetime.utcnow())

# @app.route('/api/test/hello', method='GET')
# def api_test_hello():
#     return "hello world from ..."
#     # logging.debug("IN api_test_rand()")
#     # bs = get_random_byte_string(16)
#     # logging.info(bs)
#     # hs = byte_string_to_hex_string(bs)
#     # return hs[:8]
