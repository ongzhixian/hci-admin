################################################################################
# Modules and functions import statements
################################################################################

import logging

from datetime import datetime, timedelta

from helpers.app_runtime import app, app_settings, app_secrets
from helpers.app_helper import view, get_model, require_authentication

from modules.security import aes_encrypt_as_hex
from modules.datastore import account_id_exists, add_user, hci_db, hci_firestore

from flask import request, make_response, redirect

################################################################################
# Routes
################################################################################

@app.route('/')
def webroot_get():
    logging.info("In webroot_get()")
    view_model = get_model()
    return view(view_model)

@app.route('/about')
@require_authentication
def webroot_about_get():
    logging.info("In webroot_about_get()")
    view_model = get_model()
    return view(view_model)

@app.route('/contact')
def webroot_contact_get():
    logging.info("In webroot_contact_get()")
    view_model = get_model()
    return view(view_model)

@app.route('/login')
def webroot_login_get():
    logging.info("In webroot_login_get()")
    view_model = get_model()
    view_model["google_client_id"] = app_settings["application"]["google_client_id"]
    if view_model["valid_app_token"]:
        return view(view_model, view_path="site/webroot_get.html")
    return view(view_model)

@app.route('/login', methods=['POST'])
def webroot_login_post():
    logging.info("In webroot_login_post()")

    form_username = request.form['input_email']
    form_password = request.form['input_password']

    if 'input_remember' in request.form.keys():
        form_remember = request.form['input_remember']
    else:
        form_remember = None
        

    view_model = get_model()

    view_model["valid_app_token"] = True

    # return view(view_model, view_path="site/webroot_get.html")
    # return view(view_model)
    
    # Username|CreatedDate
    username = form_username.strip()
    start_date = datetime.utcnow()
    expiry_date = start_date + timedelta(days=1) 

    cookie_text = "{0}|{1}|{2}".format(form_username, start_date.strftime("%Y%m%d"), expiry_date.strftime("%Y%m%d"))
    crypto_struct = {
        'key' : app_secrets['login']['aes_key_hex'],
        'iv' : app_secrets['login']['aes_iv_hex']
    }
    cipher_text = aes_encrypt_as_hex(crypto_struct, cookie_text)

    # Use this if we want to set cookie
    if 'from' in request.args:
        resp = redirect(request.args['from'])
    else:
        # Default 
        resp = make_response(view(view_model, view_path="site/webroot_get.html"))

    resp.set_cookie(app_settings['application']['app_token'], cipher_text)
    return resp


@app.route('/logout')
def webroot_logout_get():
    logging.info("In webroot_logout_get()")
    view_model = get_model()
    view_model["is_auth"] = False
    view_model["valid_app_token"] = False
    resp = make_response(view(view_model, view_path="site/webroot_logout_get.html"))
    resp.set_cookie(app_settings['application']['app_token'], '', expires=0)
    return resp


@app.route('/void-cookies')
def webroot_void_cookies_get():
    logging.info("In webroot_void_cookies_get()")
    resp = make_response('/')
    resp.set_cookie(app_settings['application']['app_token'], '', expires=0)
    return resp


@app.route('/authorize', methods=['POST'])
def webroot_authorize_post():
    logging.info("In webroot_authorize_post()")

    from google.oauth2 import id_token
    from google.auth.transport import requests

    if 'idtoken' not in request.form.keys():
        return

    token = request.form['idtoken']
    google_client_id = app_settings["application"]["google_client_id"]

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), google_client_id)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        # account_id = id_info['sub'] # Not using this anymore; using email

        # TODO:
        # If the user no in user database, save new user record from the information in the ID token payload
        # Else establish a session for the user
        #if not account_id_exists(account_id):
        fsdb = hci_firestore()
        db = hci_db()
        user = db.add_user(id_info['email'])
        user = fsdb.add_user(id_info['email'])
        
        start_date = datetime.utcnow()
        expiry_date = start_date + timedelta(days=1) 

        cookie_text = "{0}|{1}|{2}".format(user['user_id'], start_date.strftime("%Y%m%d"), expiry_date.strftime("%Y%m%d"))
        crypto_struct = {
            'key' : app_secrets['login']['aes_key_hex'],
            'iv' : app_secrets['login']['aes_iv_hex']
        }
        cipher_text = aes_encrypt_as_hex(crypto_struct, cookie_text)

        # Use this if we want to set cookie
        # if 'from' in request.args:
        #     resp = redirect(request.args['from'])
        # else:
        #     # Default 

        from urllib.parse import urlparse, parse_qs
        # parsed_url = urlparse(URL)
        
        query_string = request.query_string.decode("UTF8")

        if len(query_string) > 0:
            x = parse_qs(request.query_string.decode("UTF8"))
            resp = make_response(''.join(x['from']) )
        else:
            resp = make_response("/")
        resp.set_cookie(app_settings['application']['app_token'], cipher_text)
        return resp
    except ValueError:
        # Invalid token
        pass
        
    # view_model = get_model()
    # if view_model["valid_app_token"]:
    #     return view(view_model, view_path="site/webroot_get.html")
    # return view(view_model)
    # view_model = get_model()
    # view_model["is_auth"] = False
    # view_model["valid_app_token"] = False
    # resp = make_response(view(view_model, view_path="site/webroot_logout_get.html"))
    # resp.set_cookie(app_settings['application']['app_token'], '', expires=0)
    # return resp
