################################################################################
# Modules and functions import statements
################################################################################

import logging

from datetime import datetime, timedelta
from io import BytesIO

from helpers.app_runtime import app, app_settings, app_secrets
from helpers.app_helper import view, get_model, require_authentication

from modules.security import aes_encrypt_as_hex
from modules.datastore import account_id_exists, add_user
from modules.datastore import hci_db, hci_firestore

from flask import request, make_response, redirect, send_file, abort

from PyPDF2 import PdfFileWriter, PdfFileReader

__MODULE__ = "sampleApps"

################################################################################
# Routes
################################################################################

# @app.route('/administration')
# def webroot_pdf_splitter_get():
#     logging.info("In webroot_pdf_splitter_get()")
#     view_model = get_model()
#     db = hci_db()
#     return view(view_model)

@app.route('/sampleApps/test')
def sampleApps_test_get():
    logging.info("In sampleApps_test_get()")

    view_model = get_model()

    db = hci_db()
    projects = db.get_owned_projects(view_model['user_id'])
    
    view_model["projects"] = projects
    return view(view_model)
