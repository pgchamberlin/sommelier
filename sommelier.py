#!python
from src.wines import WineBroker
from flask import Flask, request, Response, jsonify, json
app = Flask(__name__)
broker = WineBroker()

def sommelier_response(name, content, meta={}):
    response = json.dumps({ name: content, 'meta': meta })
    return Response(response.decode('unicode-escape'), status=200, mimetype='application/json; charset=utf-8')

@app.route('/')
def sommelier_index():
    return "index"

@app.route('/wines', defaults = {'page': 1}, methods = ['GET'])
@app.route('/wines/<int:page>', methods = ['GET'])
def sommelier_wines(page):
    records = broker.getPage(page)
    numpages = broker.getNumPages()
    return sommelier_response('wines', records, { 'numpages': numpages })

@app.route('/wine/<wineid>', methods = ['GET','POST'])
def sommelier_wine(wineid):
    record = broker.getWine(wineid)
    return get_sommelier_response('wine', record)

@app.route('/users', methods = ['GET'])
def sommelier_users():
    return 'list of users'

@app.route('/user/new', methods = ['GET', 'POST'])
def sommelier_users():
    return 'list of users'

@app.route('/user/authenticate', methods = ['GET','POST'])
def sommelier_authenticate():
    return 'authenticate user'

@app.route('/user/deauthenticate', methods = ['GET'])
def sommelier_deauthenticate():
    return 'deauthenticate user'

@app.route('/user/<username>', methods = ['GET','POST'])
def sommelier_user():
    return 'individual user: %s' % username

if __name__ == '__main__':
    app.run(debug=True)

