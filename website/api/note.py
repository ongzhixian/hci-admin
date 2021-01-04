# 
################################################################################
# Modules and functions import statements
################################################################################

import logging
from helpers.app_runtime import app
from helpers.app_helper import view, get_model

# from modules.message import add_message

################################################################################
# Setup routes
################################################################################

@app.route('/api/note/search', methods=['GET', 'POST'])
def api_note_search(errorMessages=None):

    logging.info("In api_note_search()")

    #sqlite_file = 'D:/data/sqlite3/url_kb.sqlite3'
    sqlite_file = 'C:/Users/zong/Documents/PowerShell/url_kb.sqlite3'

    # with sqlite3.connect(sqlite_file) as conn:
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM topic ;")
    # while True:
    #     all = cur.fetchmany(batch_size)
    #     if len(all) > 0:
    #         print(len(all))
    #     else:
    #         break
    # cur.close()


    # add_message("hello world 2")
    #D:\data\sqlite3\url_kb.sqlite3

    return "OK"
    #return str(datetime.utcnow())
