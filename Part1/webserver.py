from flask import Flask, jsonify, request
import json

HOST = '0.0.0.0'
PORT = 5000
app = Flask(__name__)

@app.before_request
def open_file():
    app.ticket_file = open('data.json',encoding='utf-8')
    app.ticket_data = json.load(app.ticket_file)

@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    if len(app.ticket_data) > 0:
        return jsonify(app.ticket_data)
    else:
        return 'No Tickets Found', 404

if __name__ == '__main__':
    app.run(host=HOST,port=PORT,debug=True)
