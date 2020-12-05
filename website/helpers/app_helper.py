################################################################################
# Modules and functions import statements
################################################################################

import logging
import sys

from datetime import datetime

from flask import url_for, get_flashed_messages, request, redirect
from helpers.app_runtime import jinja2_env, app_settings, app_secrets
from modules.security import aes_decrypt_from_hex

################################################################################
# Functions
################################################################################

def get_model(cookie_json=None):
    caller = sys._getframe(1)                       # '_getframe(1)' gets previous stack; 
                                                    # '_getframe()' gets current stack
    caller_name = caller.f_code.co_name             # returns 'view_home'
    module_name = caller.f_globals['__name__']      # returns 'modules.default_routes'
    package_name = caller.f_globals['__package__']  # returns 'modules'

    context = cookie_json if cookie_json is not None else {}
    context['url_for'] = url_for                            # function for Flask
    context['get_flashed_messages'] = get_flashed_messages  # function for Flask
    context['app_settings'] = app_settings                  # make application settings available
    context['view_name'] = caller_name
    context['view_module'] = module_name
    context['view_package'] = package_name
    context['view_id'] = "{0}.{1}".format(module_name, caller_name)
    # Authentication cookie check
    app_token = request.cookies.get(app_settings['application']['app_token'])
    # view_model["google_client_id"] = app_settings["application"]["google_client_id"]
    context['google_client_id'] = app_settings["application"]["google_client_id"]
    logging.info(app_token)
    (is_token_valid, tokens) = is_valid_app_token(app_token)
    context['valid_app_token'] = is_token_valid
    if tokens is not None:
        context["username"] = tokens[0]
    else:
        context["username"] = "UNKNOWN"
    # if is_valid_app_token(app_token):
    #     context['valid_app_token'] = True
    # else:
    #     context['valid_app_token'] = False
    # context['auth_cookie'] = request.cookies.get(appconfig["application"]["auth_cookie_name"])
    # context['current_datetime'] = datetime.now()
    # context = {
    #     'auth_cookie'       : request.cookies.get(appconfig["application"]["auth_cookie_name"]),
    #     'current_datetime'  : datetime.now()
    # }
    return context

def view(model=None, view_path=None):
    if view_path is None:
        caller = sys._getframe(1)                       # '_getframe(1)' gets previous stack; 
                                                        # '_getframe()' gets current stack
        caller_name = caller.f_code.co_name             # returns 'view_home'
        module_name = caller.f_globals['__name__']      # returns 'modules.default_routes'
        package_name = caller.f_globals['__package__']  # returns 'modules'

        view_path = module_name.split('.')
        view_path.remove(package_name)
        view_path.append("{0}.html".format(caller_name))
        view_path = '/'.join(view_path)                 # returns 'default_routes/view_home.html

    logging.info("fetching view [{0}]".format(view_path))

    if model is None:
        model = get_model()

    return jinja2_env.get_template(view_path).render(model)


def is_valid_app_token(app_token):
    if not app_token:
        return (False, None)

    try:
        crypto_struct = {
            'key' : app_secrets['login']['aes_key_hex'],
            'iv' : app_secrets['login']['aes_iv_hex']
        }
        plain_text = aes_decrypt_from_hex(crypto_struct, app_token)
        tokens = plain_text.split("|")
        expiry_date = datetime.strptime(tokens[2], "%Y%m%d")
        logging.info("{0} vs {1}".format(expiry_date, datetime.utcnow()))
        if datetime.utcnow() > expiry_date:
            return (False, None)
        return (True, tokens)
    except ValueError:
        return (False, None)


########################################
# Decorators
########################################

def require_authentication(fn):
    logging.info("In require_authentication(%s)" % str(fn))
    def wrapper(*args, **kwargs):
        app_token = request.cookies.get(app_settings['application']['app_token'])
        
        if not app_token:
            logging.info(app_token)
            return redirect("/login?from={0}".format(request.path))
        
        # Else test app_token
        try:
            crypto_struct = {
                'key' : app_secrets['login']['aes_key_hex'],
                'iv' : app_secrets['login']['aes_iv_hex']
            }
            plain_text = aes_decrypt_from_hex(crypto_struct, app_token)
            
            tokens = plain_text.split("|")
            expiry_date = datetime.strptime(tokens[2], "%Y%m%d")
            if datetime.utcnow() > expiry_date:
                #expired
                return redirect("/login?from={0}".format(request.path))

            # claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            # from modules.registry import create_auth_user
            # create_auth_user(claims['email'], claims['name'])
            # if 'user_claims' not in g:
            #     g.user_claims = claims
        except ValueError as error:
            return redirect("/login?from={0}".format(request.path))

        return fn(*args, **kwargs)

    # Renaming the function name
    # Otherwise it gives a very odd (misleading) error as follows:
    # AssertionError: View function mapping is overwriting an existing endpoint function: wrapper
    wrapper.__name__ = fn.__name__
    return wrapper

################################################################################
# Export module variables
################################################################################
 
 # N/A

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    pass
