################################################################################
# Modules and functions import statements
################################################################################

import logging
from uuid import uuid4
from bson.objectid import ObjectId
from pymongo import MongoClient


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

def get_mongodb_client():
    client = MongoClient("mongodb+srv://USERNAME:PASSWORD@cluster0.vog3o.mongodb.net/hci?retryWrites=true&w=majority")
    # post = client.db.message.find_one({'_id': ObjectId('5fc9c9752fca7731bb2f92ac')})
    message = client['hci']['message'].find_one()
    return client

def add_message():
    from datetime import datetime
    message = {
        "author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.utcnow()
    }
    c = get_mongodb_client()
    messages = c['hci']['message']
    message_id = messages.insert_one(message).inserted_id
    return message


def find_message():
    c = get_mongodb_client()
    messages = c['hci']['message']
    message = messages.find_one({"author": "Mike"})
    return message

