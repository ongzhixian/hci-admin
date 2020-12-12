# 
################################################################################
# Modules and functions import statements
################################################################################

import logging
from helpers.app_runtime import app
from helpers.app_helper import view, get_model

from flask import request, make_response, redirect, send_file

from modules.datastore import hci_db, hci_firestore

# from modules.message import add_message

################################################################################
# Setup routes
################################################################################

@app.route('/api/administration', methods=['GET', 'POST'])
def api_administration(errorMessages=None):

    logging.info("In api_administration()")
    
    application_name = request.form["application_name"]

    db = hci_firestore()
    user_list = db.get_application_users(application_name)

    return user_list

    return "OK"


@app.route('/api/admin', methods=['GET', 'POST'])
def api_admin(errorMessages=None):

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
