# Message
# Should perform the following operations:
# 1.  Add message
# 2.  Get message
# 3.  Update message
# 4.  Remove message

################################################################################
# Modules and functions import statements
################################################################################

import logging
from enum import Enum
from queue import Queue
from datetime import datetime
from google.cloud import datastore

################################################################################
# Module variables
################################################################################

# datastore_client = datastore.Client()

db = datastore.Client(namespace="zxsh")
entity_key_queue = Queue()

################################################################################
# Define functions
################################################################################

def get_new_entity_key():
    if entity_key_queue.empty():
        try:
            #partial_key = db.key('db', 'blazer_loan', 'loan_request')
            # parent_key = db.key('message_list', 'zhixian')
            # partial_key = db.key('message', parent=parent_key)
            partial_key = db.key('message_list', 'zhixian', 'message')
            keys = db.allocate_ids(partial_key, 10)
            for key in keys:
                entity_key_queue.put(key)
        except Exception as e:
            logging.error(e)

    return entity_key_queue.get()

def add_message(data):
    try:
        op_datetime = datetime.utcnow()
        with db.transaction():
            key = get_new_entity_key()
            # parent_key = db.key('zxsh', 'message_list')
            # key = db.key('Task', 'sample_task', parent=parent_key)
            ent = db.get(key)
            if not ent:
                ent = datastore.Entity(key)
                ent.update({
                    'body'      : data,
                    # 'cre_date'  : op_datetime,
                    'status'    : 0
                })
                db.put(ent)
                logging.info("Add entity")
                #print("Create loan request: {0}".format(data['nric']))
    except Exception as e:
        logging.error(e)

def get_message(data):
    pass
    # try:
    #     op_datetime = datetime.utcnow()
    #     with db.transaction():
    #         key = get_new_entity_key()
    #         # parent_key = db.key('zxsh', 'message_list')
    #         # key = db.key('Task', 'sample_task', parent=parent_key)
    #         ent = db.get(key)
    #         if not ent:
    #             ent = datastore.Entity(key)
    #             ent.update({
    #                 'body'      : data,
    #                 # 'cre_date'  : op_datetime,
    #                 'status'    : 0
    #             })
    #             db.put(ent)
    #             #print("Create loan request: {0}".format(data['nric']))
    # except Exception as e:
    #     logging.error(e)

