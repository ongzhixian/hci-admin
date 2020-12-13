# 
################################################################################
# Modules and functions import statements
################################################################################

import json
import logging
from helpers.app_runtime import app
from helpers.app_helper import view, get_model

from flask import request, make_response, redirect, send_file, abort

from modules.datastore import hci_db, hci_firestore

# from modules.message import add_message

################################################################################
# Setup routes
################################################################################

@app.route('/api/administration', methods=['GET', 'POST'])
def api_administration(errorMessages=None):

    if request.method != 'POST' or not request.is_json:
        logging.info("message=Invalid request|method={0}|is_json={1}|src={2}|event=end".format(request.method, request.is_json, __name__))
        abort(404, {
            "is_api" : True,
            "message" : "Invalid request",
            "src" : __name__
        })

    view_model = get_model()

    #db = hci_firestore()

    #has_access = db.has_access(__MODULE__, view_model["user_id"])

    user_id = view_model['user_id']
    
    application_name = request.json["application_name"]
    user_email = request.json["user_email"]
    action = request.json["action"]

    logging.info("user_id={0}|application_name={1}|user_email={2}|action={3}".format(user_id, application_name, user_email, action))

    if action == "adsd_application_user":
        db = hci_firestore()
        
        db.add_application_access(application_name, user_id)
    
        #db.add_application_user(application_name, user_email)
        # db.assign_application(application_name, user_email)
        #user_list = db.get_application_users(application_name)

    return "OK"
    

@app.route('/api/administration/test', methods=['GET', 'POST'])
def api_administration_test(errorMessages=None):

    logging.info("In api_administration_test()")
    
    db = hci_firestore()
    #db.find_user("overxianz@gmail.com")
    #db.add_user("overxianz@gmail.com")
    #db.assign_application("dnmo_app", "overxianz@gmail.com")

    #return str(db.has_access("dnmo_app", "overxianz@gmail.com"))
    #db.remove_application_access("dnmo_app", "overxianz@gmail.com")
    db.add_application_access("dnmo_app", "dummy_user")

    return "ok"




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
