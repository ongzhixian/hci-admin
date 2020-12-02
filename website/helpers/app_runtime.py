################################################################################
# Modules and functions import statements
################################################################################

import logging
import json
import sys

from flask import Flask

from jinja2 import Template, Environment, FileSystemLoader
from os import getenv

################################################################################
# Functions
################################################################################

def get_app_settings():
    logging.debug("In get_app_settings()")
    app_settings_file = open('app-settings.json')
    app_settings = json.load(app_settings_file)

    if getenv('GAE_ENV', '').startswith('standard'):
        app_settings["IS_HOSTED"] = True
    else:
        app_settings["IS_HOSTED"] = False

    return app_settings

def get_app_secrets():
    logging.debug("In get_app_secrets()")
    app_secrets_file = open('app-secrets.json')
    app_secrets = json.load(app_secrets_file)
    return app_secrets

def setup_jinja2_env():
    logging.debug("In setup_jinja2_env()")
    env = Environment(loader = FileSystemLoader('./views'))
    return env

################################################################################
# Export module variables
################################################################################

app = Flask("hci-admin", static_url_path='/', static_folder='wwwroot',)
app_settings = get_app_settings()
app_secrets = get_app_secrets()
jinja2_env = setup_jinja2_env()

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    pass
