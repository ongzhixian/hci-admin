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

from flask import request, make_response, redirect, send_file

from PyPDF2 import PdfFileWriter, PdfFileReader

################################################################################
# Routes
################################################################################

# @app.route('/administration')
# def webroot_pdf_splitter_get():
#     logging.info("In webroot_pdf_splitter_get()")
#     view_model = get_model()
#     db = hci_db()
#     return view(view_model)

@app.route('/administration/test')
def administration_test_get():
    logging.info("In administration_test_get()")

    view_model = get_model()

    db = hci_db()
    projects = db.get_owned_projects(view_model['user_id'])
    
    view_model["projects"] = projects
    return view(view_model)

@app.route('/administration/roles')
def administration_roles_get():
    logging.info("In administration_roles_get()")

    view_model = get_model()

    # db = hci_db()
    # projects = db.get_owned_projects(view_model['user_id'])    
    # view_model["projects"] = projects
    db = hci_firestore()
    view_model["role_list"] = db.get_roles()

    return view(view_model)

@app.route('/administration/roles', methods=['POST'])
def administration_roles_post():
    logging.info("In administration_roles_post()")

    role_name   = request.form['role_name']
    form_action  = request.form['action']

    if form_action == "add_role":
        db = hci_firestore()
        db.add_role(role_name)

    view_model = get_model()

    # db = hci_db()
    # projects = db.get_owned_projects(view_model['user_id'])
    
    # view_model["projects"] = projects
    return view(view_model, view_path="administration/administration_roles_get.html")
    #return view(view_model)

@app.route('/administration/applications')
def administration_applications_get():
    logging.info("In administration_applications_get()")

    view_model = get_model()
    db = hci_firestore()
    view_model["application_list"] = db.get_applications()

    return view(view_model)


@app.route('/administration/applications', methods=['POST'])
def administration_applications_post():
    logging.info("In administration_applications_post()")

    view_model = get_model()

    application_name   = request.form['application_name']
    form_action  = request.form['action']

    if form_action == "add_application":
        db = hci_firestore()
        db.add_application(application_name)

    return view(view_model, view_path="administration/administration_applications_get.html")


@app.route('/administration/assignments')
def administration_assignments_get():
    logging.info("In administration_assignments_get()")

    view_model = get_model()
    db = hci_firestore()
    view_model["application_list"] = db.get_applications()

    return view(view_model)