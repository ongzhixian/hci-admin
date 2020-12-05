################################################################################
# Modules and functions import statements
################################################################################

import logging
from datetime import datetime
from uuid import uuid4

from bson.objectid import ObjectId
from pymongo import MongoClient

from helpers.app_runtime import app, app_settings, app_secrets

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

def get_mongodb_client(database_name):
    return MongoClient(app_secrets["mongodb"][database_name])

def add_message():
    
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

def add_project():
    client = get_mongodb_client('hci')
    

class hci_db():
    def __init__(self):
        logging.info("class=hci_db method=__init__ event=begin")
        self.client = get_mongodb_client('hci')
        self.db = self.client['hci']
        logging.info("class=hci_db method=__init__ event=end")

    def project_exist(self, owner, title):
        projects = self.db['project']
        doc_count = projects.count_documents({"owner": {"$in":[owner]}, "title": title } )
        return project_exist > 0

    def find_project(self, owner, title):
        projects = self.db['project']
        project = projects.find_one({"owner": {"$in":[owner]}, "title": title } )
        return project

    def get_project_info(self, id):
        projects = self.db['project']
        project_info = projects.find_one({"_id": ObjectId(id)}, {"file_bytes": 0})
        return project_info

    def get_owned_projects(self, owner):
        projects = self.db['project']
        cursor = projects.find({"owner": {"$in":[owner]} }, {"title": 1, "filename": 1, "upd_dt": 1})
        owned_projects = []
        for doc in cursor:
            owned_projects.append(doc)
        return owned_projects

    def update_project(self, id, split_method, n_page, terminator_text):
        projects = self.db['project']
        newvalues = { "$set": { "split_method": split_method, "n_page": n_page, "terminator_text": terminator_text } }
        projects.update_one({"_id": ObjectId(id)}, newvalues)
        return True

    def get_file(self, id):
        projects = self.db['project']
        project_file = projects.find_one({"_id": ObjectId(id)}, {"filename" : 1, "file_bytes": 1})
        return (project_file['filename'], project_file['file_bytes'])

        
    #'PUBLIC', project_title, project_file_name, project_file_bytes
    def add_project(self, owner, title, file_name=None, file_bytes=None, file_size=0):

        logging.info("class=hci_db method=add_project event=begin")

        projects = self.db['project']
        
        project = {
            "title"         : title,
            "owner"         : [owner],
            "tags"          : ["pdf-splitter", "python", "pymongo"],
            "filename"      : file_name,
            "file_bytes"    : file_bytes,
            "file_size"     : file_size,
            "cre_dt"        : datetime.utcnow(),
            "upd_dt"        : datetime.utcnow()
        }

        if self.find_project(owner, title) is None:
            logging.info("proj not exist, insert")
            project_id = projects.insert_one(project).inserted_id
        else:
            logging.info("exist, do nothing")
            project_id = None
        
        logging.info("class=hci_db method=add_project event=end")
        return project_id
