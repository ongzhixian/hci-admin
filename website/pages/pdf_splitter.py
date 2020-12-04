################################################################################
# Modules and functions import statements
################################################################################

import logging

from datetime import datetime, timedelta

from helpers.app_runtime import app, app_settings, app_secrets
from helpers.app_helper import view, get_model, require_authentication

from modules.security import aes_encrypt_as_hex
from modules.datastore import account_id_exists, add_user

from flask import request, make_response, redirect

################################################################################
# Routes
################################################################################

@app.route('/pdf-splitter/projects')
def pdf_splitter_projects_get():
    logging.info("In pdf_splitter_projects_get()")
    view_model = get_model()
    from modules.datastore import get_mongodb_client
    client = get_mongodb_client()
    return view(view_model)

@app.route('/pdf-splitter/create-project')
def pdf_splitter_create_project_get():
    logging.info("In pdf_splitter_create_project_get()")
    view_model = get_model()
    from modules.datastore import get_mongodb_client
    client = get_mongodb_client()
    return view(view_model)
