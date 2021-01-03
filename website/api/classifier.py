# 
################################################################################
# Modules and functions import statements
################################################################################

import json
import logging
from helpers.app_runtime import app
from helpers.app_helper import view, get_model

import sqlite3
# from modules.message import add_message

################################################################################
# Setup routes
################################################################################

@app.route('/api/classifier/search', methods=['GET', 'POST'])
def api_classifier_search(errorMessages=None):

    logging.info("In api_kb_search()")

    sql = """
    SELECT netloc, sum(count) AS link_count FROM parsed_urls
    GROUP BY netloc
    ORDER BY link_count DESC
    LIMIT 100;"""

    all = get_data(sql)

    return json.dumps(all)
    #return str(datetime.utcnow())

def get_data(sql):
    sqlite_file = 'D:/data/sqlite3/url_kb.sqlite3'
    with sqlite3.connect(sqlite_file) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        all = cur.fetchall()
        cur.close()
    return all


# @app.route('/api/msg', methods=['GET', 'POST'])
# def api_msg(errorMessages=None):

#     logging.info("In api_msg()")

#     # add_message("hello world 2")

#     return "OK"
    #return str(datetime.utcnow())

# @app.route('/api/test/hello', method='GET')
# def api_test_hello():
#     return "hello world from ..."
#     # logging.debug("IN api_test_rand()")
#     # bs = get_random_byte_string(16)
#     # logging.info(bs)
#     # hs = byte_string_to_hex_string(bs)
#     # return hs[:8]
