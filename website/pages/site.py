################################################################################
# Modules and functions import statements
################################################################################

import logging

from datetime import datetime, timedelta

from helpers.app_runtime import app, app_settings, app_secrets
from helpers.app_helper import view, get_model, require_authentication

from modules.security import aes_encrypt_as_hex

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
