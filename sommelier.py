#!python
import sommelier.wines
import sommelier.users
from flask import Flask, Response, jsonify, json
app = Flask(__name__)

@app.route('/')
def sommelier_index():
  return "index"

@app.route('/authenticate', methods = ['GET','POST'])
def sommelier_authenticate():
  return 'authenticate'

@app.route('/deauthenticate', methods = ['GET'])
def sommelier_deauthenticate():
  return 'deauthenticate'

@app.route('/wines', defaults = {'page': 1}, methods = ['GET'])
@app.route('/wines/<int:page>', methods = ['GET'])
def sommelier_wines(page):
  broker = sommelier.wines.WineBroker()
  records = broker.getPage(page)
  numpages = broker.getNumPages()
  response = json.dumps({ 'wines': records, 'numpages': numpages })
  return Response(response.decode('unicode-escape'), status=200, mimetype='application/json; charset=utf-8')

@app.route('/wine/<wineid>', methods = ['GET','POST'])
def sommelier_wine():
  return 'single wine: %s' % wineid

@app.route('/users', methods = ['GET'])
def sommelier_users():
  return 'list of users'

@app.route('/useri/<username>', methods = ['GET','POST'])
def sommelier_user():
  return 'individual user: %s' % username

if __name__ == '__main__':
  app.run(debug=True)

