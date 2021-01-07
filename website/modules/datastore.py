################################################################################
# Modules and functions import statements
################################################################################

import logging
from datetime import datetime
from uuid import uuid4

from bson.objectid import ObjectId
from pymongo import MongoClient

from google.cloud import firestore

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
    

########################################
# Firestore
########################################
class hci_firestore():
    """Represent an HCI Firestore

    Attributes:
        db (firestore.Client): Points to an instance of Firestore client

    """

    def __init__(self):
        """Initializes Firestore client as db

        Args:
            None

        """
        logging.info("class=hci_firestore method=__init__ event=begin")
        self.db = firestore.Client()
        logging.info("class=hci_firestore method=__init__ event=end")

    ########################################
    # User functions
    ########################################

    # def user_email_exists(self, email):
    #     doc = self.db.collection('user').document(email).get() # DocumentSnapshot
    #     return doc.exists
        # doc_list = self.db.collection('user').where('email', '==', email).limit(1).get()
        # return len(doc_list) > 0
    # def get_user(self, email, asDict=True):
    #     doc_list = self.db.collection('user').where('email', '==', email).limit(1).get()
    #     if len(doc_list) > 0:
    #         if asDict:
    #             return doc_list[0].to_dict()
    #         else:
    #             return doc_list[0]
    #     return None
    # def get_user(self, email):
    #     return self.db.collection('user').document(email).get() # DocumentSnapshot


    def get_user_ref(self, doc_id):
        """Retrieves document reference to document in user collection of matching email address

        Args:
            email: An email address

        Returns:
            DocumentReference of matching user document

        """
        return self.db.collection('user').document(doc_id) # DocumentReference

    
    def add_user(self, email_address):
        """Add or get snapshot of document in user collection of matching email address

        Args:
            email_address: An email address

        Returns:
            DocumentSnapshot of matching user document

        """

        user_id = self.find_user(email_address)
        if user_id is None:
            doc_id = str(uuid4())
            (update_time, user_id) = self.db.collection('user').add({
                'email' : email_address,
                'user_key' : doc_id
            })
        return (True, user_id)

        doc_ref = self.get_user_ref(email_address)
        if not doc_ref.get().exists:
            doc_id = str(uuid4())
            doc_ref.set({
                'email' : email_address,
                'user_id' : doc_id
            })
        return doc_ref.get()


    def find_user(self, email_address):
        """Status: dev | review | production """

        logging.info("email_address={0}|event=begin".format(email_address))

        result = None

        query = self.db.collection('user').where('email', '==', email_address).limit(1) # Query

        doc_list = query.get() # list of DocumentSnapshot

        if len(doc_list) > 0:
            result = doc_list[0].id
            
        logging.info("email_address={0}|result={1}|event=end".format(email_address, result))

        return result

    def get_user_id(self, email_address):
        """Status: dev | review | production """

        logging.info("email_address={0}|event=begin".format(email_address))

        user_id = self.find_user(email_address)

        if user_id is None: # Add user if no user_id found

            allow_to_add = True # TODO: at a later date

            if not allow_to_add:
                
                user_id = "Unknown"

            else:

                doc_id = str(uuid4())

                (update_time, user_id) = self.db.collection('user').add({
                    'email' : email_address,
                    'user_key' : doc_id
                })

        logging.info("email_address={0}|result={1}|event=end".format(email_address, user_id))

        return user_id

        

    ########################################
    # Role functions
    ########################################

    def get_roles(self):
        doc_list = self.db.collection('role').get()
        return list(map(lambda x: { "id" : x.id, "data" : x.to_dict()}, doc_list))

    # def role_exists(self, role_name):
    #     #doc_list = self.db.collection('role').where('email', '==', email).limit(1).get()
    #     # doc = self.db.collection('role').document(role_name).get()
    #     # return doc is None
    #     doc_list = self.db.collection('role').where('role_name', '==', role_name).limit(1).get()
    #     return len(doc_list) > 0

    # def get_role(self, role_name):
    #     #doc_list = self.db.collection('role').where('email', '==', email).limit(1).get()
    #     #doc_list = self.db.collection('role').document(role_name)
    #     # doc = self.db.collection('role').document(role_name).get()
    #     # return doc
    #     # if len(doc_list) > 0:
    #     #     return doc_list[0].to_dict()
    #     # return None
    #     doc_list = self.db.collection('role').where('role_name', '==', role_name).limit(1).get()
    #     if len(doc_list) > 0:
    #         return doc_list[0].to_dict()
    #     return None

    # def add_role2(self, role_name):
    #     if not self.role_exists(role_name):
    #         role_id = str(uuid4())
    #         self.db.collection('role').add({
    #             'role_name' : role_name,
    #             'role_id' : role_id
    #         })
    #     return self.get_role(role_name)

    def get_role_ref(self, role_name):
        return self.db.collection('role').document(role_name) # DocumentReference

    def add_role(self, role_name):
        doc_ref = self.get_role_ref(role_name)
        if not doc_ref.get().exists:
            doc_id = str(uuid4())
            doc_ref.set({
                'role_name' : role_name,
                'role_id' : doc_id
            })
        return doc_ref.get()


    ########################################
    # Application functions
    ########################################

    def get_applications(self):
        doc_list = self.db.collection('application').get()
        return list(map(lambda x: { "id" : x.id, "data" : x.to_dict()}, doc_list))
        # return list(map(lambda x: x.to_dict(), doc_list))

    # def application_exists(self, application_name):
    #     doc_list = self.db.collection('application').where('application_name', '==', application_name).limit(1).get()
    #     return len(doc_list) > 0

    # def get_application(self, application_name, asDict=True):
    #     doc_list = self.db.collection('application').where('application_name', '==', application_name).limit(1).get()
    #     if len(doc_list) > 0:
    #         if asDict:
    #             return doc_list[0].to_dict()
    #         else:
    #             return doc_list[0]
    #     return None

    # def add_application2(self, application_name):
    #     if not self.application_exists(application_name):
    #         application_id = str(uuid4())
    #         self.db.collection('application').add({
    #             'application_name' : application_name,
    #             'application_id' : application_id
    #         })
    #     return self.get_application(application_name)


    def get_application_ref(self, application_name):
        return self.db.collection('application').document(application_name) # DocumentReference

    def add_application(self, application_name):
        doc_ref = self.get_application_ref(application_name)
        if not doc_ref.get().exists:
            doc_id = str(uuid4())
            doc_ref.set({
                'application_name' : application_name,
                'application_id' : doc_id
            })
        return doc_ref.get()

    ########################################
    # Get x-users
    ########################################

    def get_application_users(self):
        pass

    def add_application_user(self, application_name, user_email):
        # find the record 
        user = self.get_user(user_email, False)
        application = self.get_application(application_name, False)
        if user is not None and application is not None:
            application_doc = user.reference.collection('applications').document(application.reference.id).set({})
            #application_doc.reference.update({"roles" : firestore.ArrayUnion([])})
            # import pdb
            # pdb.set_trace()
            # user.reference.update({"applications" : firestore.ArrayUnion([
            #     {
            #         "id" : application.reference.id,
            #         "roles" : firestore.ArrayUnion(['xxx'])
            #     }
            #     ])})
        else:
            logging.info("FAILED add_application_user({0}, {1})".format(application_name, user_email))
        
    def remove_application_user(self, application_name, user_email):
        # find the record 
        user = self.get_user(user_email, False)
        user.reference.update({"applications" : firestore.ArrayRemove([application_name])})

    def add_application_access(self, application_name, user_id):
        """Status: dev | review | production """

        logging.info("application_name={0}|user_id={1}|event=begin".format(application_name, user_id))

        doc_ref = self.get_user_ref(user_id)

        # we should not add if unvalid user or not exists or not allow to assign

        if not doc_ref.get().exists:

            logging.info("message=User does not exists|user_id={1}|event=end".format(application_name, user_id))
            
        else:

            app_ref = doc_ref.collection('applications').document(application_name)

            allow_to_add = True # TODO

            if not app_ref.get().exists and allow_to_add:

                logging.info("message=Add user|allow_to_add={0}|add=|event=end".format(allow_to_add))

                result = app_ref.set({}) # Empty document as placeholder

            else:

                logging.info("message=Not allow to add|allow_to_add={0}|event=end".format(allow_to_add))
            

    def remove_application_access(self, application_name, user_id):
        """Status: dev | review | production """
        doc_ref = self.get_user_ref(user_id)

        # we should not add if unvalid user or not exists or not allow to assign

        if not doc_ref.get().exists:
            is_allowed_action = True # TODO

            if not is_allowed_action:
                return # Do nothing

            app_ref = doc_ref.collection('applications').document(application_name)
            if app_ref.get().exists:
                app_ref.delete()
        
    def has_access(self, application_name, user_id):
        """Status: dev | review | production """
        doc_ref = self.get_user_ref(user_id)
        app_ref = doc_ref.collection('applications').document(application_name)
        return app_ref.get().exists

    def get_user_list(self):
        """Status: dev | review | production """
        doc_list = self.db.collection('user').get() # collectionReference
        return list(map(lambda x: { "id" : x.id, "data" : x.to_dict()}, doc_list))

########################################
# MongoDb 
########################################
class hci_db():
    def __init__(self):
        logging.info("class=hci_db method=__init__ event=begin")
        self.client = get_mongodb_client('hci')
        self.db = self.client['hci']
        logging.info("class=hci_db method=__init__ event=end")

    ########################################
    # User / Role functions
    ########################################

    def user_email_exists(self, email):
        users = self.db['user']
        doc_count = users.count_documents({"email": email } )
        return doc_count > 0

    def get_user(self, email):
        users = self.db['user']
        user = users.find_one({"email": email})
        return user

    def add_user(self, email):
        if not self.user_email_exists(email):
            user_id = str(uuid4())
            user = {
                'email' : email,
                'user_id' : user_id
            }
            users = self.db['user']
            user = users.insert_one(user)
        return self.get_user(email)

    ########################################
    # PDF-splitter projects related functions
    ########################################

    def project_exist(self, owner, title):
        projects = self.db['project']
        doc_count = projects.count_documents({"owner": {"$in":[owner]}, "title": title } )
        return doc_count > 0

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

    def delete_project(self, id):
        projects = self.db['project']
        projects.delete_one({"_id": ObjectId(id)})
        return True


    def get_file(self, id):
        projects = self.db['project']
        project_file = projects.find_one({"_id": ObjectId(id)}, {"filename" : 1, "file_bytes": 1})
        return (project_file['filename'], project_file['file_bytes'])

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


class note_db():
    def __init__(self):
        logging.info("class=note_db method=__init__ event=begin")
        self.client = get_mongodb_client('hci')
        self.db = self.client['hci']
        logging.info("class=note_db method=__init__ event=end")
    
    def notes_exists(self):
        notes = self.db['note']
        doc_count = notes.count_documents()
        return doc_count > 0

    def tag_exist(self, name):
        tags = self.db['tag']
        logging.info("Finding {0}".format(name))
        doc_count = tags.count_documents({"name": name })
        logging.info("Finding {0} - count".format(name, doc_count))
        return doc_count > 0

    def find_tags(self, name):
        tags = self.db['tag']
        docs = tags.find({"name": name } )
        return docs

    def add_tag(self, name):
        tags = self.db['tag']
        
        tag = {
            "name"          : name,
            "cre_dt"        : datetime.utcnow(),
            "upd_dt"        : datetime.utcnow()
        }

        if not self.tag_exist(name):
            logging.info("proj not exist, insert")
            doc_id = tags.insert_one(tag).inserted_id
        else:
            logging.info("exist, do nothing")
            doc_id = None
        return doc_id

    def add_note(self, title, content):
        logging.info("add_note")

        notes = self.db['note']
        note = {
            "title"         : title,
            "content"       : content,
            "cre_dt"        : datetime.utcnow(),
            "upd_dt"        : datetime.utcnow()
        }

        doc_id = notes.insert_one(note).inserted_id

        logging.info("doc_id {0}".format(doc_id))

        return doc_id

    def update_note(self, doc_id, title, content):
        logging.info("update_note")

        notes = self.db['note']
        doc = notes.find_one({"_id": ObjectId(doc_id)})

        if doc is not None:
            update_status = notes.update_one({"_id": ObjectId(doc_id)}, { "$set": {
                "title" : title,
                "content" : content 
            }})
            return doc_id if update_status.modified_count > 0 else None

        return None
