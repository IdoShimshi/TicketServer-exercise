from flask import Flask, jsonify, request, g
import json
from datetime import datetime
import sqlite3

HOST = '0.0.0.0'
PORT = 5000
app = Flask(__name__)
conn = None

# connects to db and creates tickets table from data.json
# if db already exists, returns
def createDBIfNeeded():
    conn = sqlite3.connect('TicketSystem.db')
    c = conn.cursor()
    listOfTables = c.execute( #check if tickets already exists
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name='tickets'; """).fetchall()
    if listOfTables != []:
        return

    c.execute('''CREATE TABLE tickets
             (id TEXT PRIMARY KEY,
              title TEXT,
              content TEXT,
              userEmail TEXT,
              creationTime timestamp);''')
    conn.commit()
    with open('../../data.json',encoding='utf-8') as f:
        data = json.load(f)
        for ticket in data:
            c.execute('''INSERT INTO tickets
                        (id, title, content, userEmail, creationTime)
                        VALUES (?, ?, ?, ?, ?)''',
                    (ticket['id'],
                    ticket['title'],
                    ticket['content'],
                    ticket['userEmail'],
                    datetime.fromtimestamp(ticket['creationTime']/1000)))

    conn.commit()
    conn.close()

# Gets c, cursor connected to the TicketSystem DB
#      searchPhrase, None or a string to search for in the title, content and email fields
#      searchFrom, None or a string of date to search from
#      searchTo, None or a string of date to search To
# Returns a list of every ticket that matches the search parameters
def searchTickets(c, searchPhrase, searchFrom, searchTo):
    searchPhrase = searchPhrase or ''
    searchFrom = searchFrom or '1970-01-01 00:00:00'
    searchTo = searchTo or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = '''SELECT * 
            FROM tickets
            where (content like ?
            or title like ?
            or userEmail like ?) 
            and creationTime BETWEEN strftime('%Y-%m-%d %H:%M:%S',?) AND strftime('%Y-%m-%d %H:%M:%S',?)
            '''
    wildcardSearch = f"%{searchPhrase}%"
    c.execute(query, [wildcardSearch, wildcardSearch, wildcardSearch, searchFrom, searchTo])

    #turns query answer to json format
    res = [dict((c.description[i][0], value) \
               for i, value in enumerate(row)) for row in c.fetchall()]

    return res

@app.before_first_request
def setup():
    createDBIfNeeded()

@app.before_request
def open_con():
    g.conn = sqlite3.connect('TicketSystem.db')

@app.teardown_request
def close_con(exec):
    if 'conn' in g:
        g.conn.close()

@app.route('/tickets', methods=['GET'])
def get_tickets():
    searchPhrase = request.args.get('search')
    searchFrom = request.args.get('from')
    searchTo = request.args.get('to')
    return jsonify(searchTickets(g.conn.cursor(), searchPhrase,searchFrom,searchTo))


if __name__ == '__main__':
    app.run(host=HOST,port=PORT,debug=True)
