################################################################################
# Modules and functions import statements
################################################################################

import logging

from datetime import datetime, timedelta

from helpers.app_runtime import app, app_settings, app_secrets
from helpers.app_helper import view, get_model, require_authentication

from modules.security import aes_encrypt_as_hex
from modules.datastore import account_id_exists, add_user
from modules.datastore import hci_db

from flask import request, make_response, redirect

################################################################################
# Routes
################################################################################

@app.route('/pdf-splitter')
def webroot_pdf_splitter_get():
    logging.info("In webroot_pdf_splitter_get()")
    view_model = get_model()
    db = hci_db()
    return view(view_model)

@app.route('/pdf-splitter/projects')
def pdf_splitter_projects_get():
    logging.info("In pdf_splitter_projects_get()")
    view_model = get_model()
    # from modules.datastore import get_mongodb_client
    # client = get_mongodb_client()
    return view(view_model)

@app.route('/pdf-splitter/create-project')
def pdf_splitter_create_project_get():
    logging.info("In pdf_splitter_create_project_get()")
    view_model = get_model()
    return view(view_model)

@app.route('/pdf-splitter/create-project', methods=['POST'])
def pdf_splitter_create_project_post():
    logging.info("In pdf_splitter_create_project_post()")

    project_title   = request.form['project_title']
    project_action  = request.form['action']
    project_file_name = None
    project_file_bytes = None
    project_file_size = 0
    
    if len(request.files) > 0:
        project_file = request.files['project_file']
        project_file_name = project_file.filename
        project_file_bytes = request.files['project_file'].stream.read()
        project_file_size = len(project_file_bytes)

    db = hci_db()
    # db.find_project('PUBLIC', project_title)
    project_id = db.add_project('PUBLIC', project_title, project_file_name, project_file_bytes, project_file_size)

    # resp = make_response(view(view_model, view_path="site/webroot_get.html"))
    if project_id is not None:
        return redirect("/pdf-splitter/project/my-project-id")
    
    view_model = get_model()
    view_model["project_title"] = project_title
    view_model["error"] = "Project title exists"
    return view(view_model, view_path="pdf_splitter/pdf_splitter_create_project_get.html")
    #return view(view_model)

@app.route('/pdf-splitter/project/<project_id>')
def pdf_splitter_project_get(project_id = None):
    logging.info("In pdf_splitter_project_get()")
    view_model = get_model()
    # from modules.datastore import get_mongodb_client
    # client = get_mongodb_client()
    return view(view_model)