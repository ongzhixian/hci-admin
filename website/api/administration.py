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

    if not request.is_json:
        return "NG"

    application_name = request.json["application_name"]
    user_email = request.json["user_email"]
    action = request.json["action"]

    if action == "add_application_user":
        db = hci_firestore()
        db.add_application_user(application_name, user_email)
        #user_list = db.get_application_users(application_name)

        return "OK"
    return "NG"


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
