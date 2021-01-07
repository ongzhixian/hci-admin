# 
################################################################################
# Modules and functions import statements
################################################################################

import json
import logging

from html.parser import HTMLParser

from helpers.app_runtime import app
from helpers.app_helper import view, get_model

from flask import request, make_response, abort

from modules.datastore import note_db
# from modules.message import add_message

################################################################################
# Setup routes
################################################################################

@app.route('/api/note/search', methods=['GET', 'POST'])
def api_note_search(errorMessages=None):

    logging.info("In api_note_search()")

    #sqlite_file = 'D:/data/sqlite3/url_kb.sqlite3'
    sqlite_file = 'C:/Users/zong/Documents/PowerShell/url_kb.sqlite3'

    search_term = None

    if 'search_text' in request.form:
        search_term = request.form['search_text']

    if search_term is not None:
        db = note_db()
        tags = db.find_tags(search_term)
        if tags.count() <= 0:
            db.add_tag(search_term)
        

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



@app.route('/api/note/save', methods=['GET', 'POST'])
def api_note_save(errorMessages=None):

    logging.info("In api_note_save()")

    content = None
    doc_id = None

    if 'content' in request.form:
        content = json.loads(request.form['content'])
    if 'doc_id' in request.form:
        doc_id = request.form['doc_id']

    html_parser = HeadingParser()
    html_parser.feed(content)
    
    title = html_parser.title if html_parser.title is not None else 'Untitled'

    logging.info("Title is {0}".format(title))

    if content is not None:
        db = note_db()

        if len(doc_id) <= 0:
            doc_id = db.add_note(title, content)
        else:
            doc_id = db.update_note(doc_id, title, content)

        return json.dumps({
            "doc_id" : str(doc_id)
        })

    return "OK"


class HeadingParser(HTMLParser):		    #create a subclass of HTMLParser which will overload handle..

    def __init__(self):
        HTMLParser.__init__(self)
        self.title = None
        self.is_h1_tag = False

    def handle_starttag(self, tag, attrs):	#Triggered when an opening tag is encountered
        self.is_h1_tag = False
        if tag == "h1":						#if the tag is &lt;h1&gt;
            self.is_h1_tag = True				#Change a variable which says we are in an header

    def handle_data(self, data):				#Triggered when data found (the content of the tag)
        if self.is_h1_tag and self.title is None:					    #Useless, used just to filter content of h1's
            self.title = data

    def handle_endtag(self, tag):				
        if tag =="h1":						
            self.is_h1_tag = False
