################################################################################
# Modules and functions import statements
################################################################################

import logging
from uuid import uuid4

################################################################################
# Module variables
################################################################################

users = []

################################################################################
# Define functions
################################################################################

def account_id_exists(account_id):
    for user in users:
        if user['account_id'] == account_id:
            return True
    return False

def user_id_exists(user_id):
    for user in users:
        if user['user_id'] == user_id:
            return True
    return False

def get_user_id(account_id):
    for user in users:
        if user['account_id'] == account_id:
            return user['user_id']

def add_user(account_id):
    if not user_id_exists(account_id):
        user_id = str(uuid4())
        user = {
            'account_id' : account_id,
            'user_id' : user_id
        }
        users.append(user)
        return user_id
    return get_user_id(account_id)