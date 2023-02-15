from flask import Flask, jsonify, request, g
import json
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000
app = Flask(__name__)

#Gets a string representing datetime
#Returns None or datetime of date_string
def parse_datetime(date_string):
    if not date_string:
        return None
    formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H', '%Y-%m-%d'] #can easily add other formats if needed
    for format in formats:
        try:
            return datetime.strptime(date_string, format)
        except ValueError:
            pass
    raise ValueError(f"No valid format found for '{date_string}'")


# Gets data, a dictionary with ticket data
#      searchPhrase, None or a string to search for in the title, content and email fields
#      searchFrom, None or a string of date to search from
#      searchTo, None or a string of date to search To
# Returns a list of every ticket that matches the search parameters
def searchTickets(data, searchPhrase, searchFrom, searchTo):
    res = []
    for ticket in data:
        dt = datetime.fromtimestamp(ticket['creationTime']/1000)
        parsedFrom = parse_datetime(searchFrom)
        parsedTo = parse_datetime(searchTo)

        # will be true if dt >= from or if from is None
        dateAfterFrom = not parsedFrom or dt >= parsedFrom 
        # will be true if dt <= to or if to is None
        dateBeforeTo = not parsedTo or dt <= parsedTo 
        # will be true if search is None or is found in any of content,title,userEmail
        foundText = not searchPhrase or any(searchPhrase in s for s in [ticket['content'], ticket['title'],ticket['userEmail']]) 

        if foundText and dateAfterFrom and dateBeforeTo:
            res.append(ticket)
    return res

@app.before_request
def open_file():
    g.ticket_file = open('../../data.json',encoding='utf-8')

@app.teardown_request
def close_file(exec):
    if 'ticket_file' in g:
        g.ticket_file.close()

@app.route('/tickets', methods=['GET'])
def get_tickets():
    searchPhrase = request.args.get('search')
    searchFrom = request.args.get('from')
    searchTo = request.args.get('to')
    if searchPhrase or searchFrom or searchTo:
        return jsonify(searchTickets(json.load(g.ticket_file), searchPhrase,searchFrom,searchTo))
    else:
        return jsonify(g.ticket_data)

    
if __name__ == '__main__':
    app.run(host=HOST,port=PORT,debug=True)
