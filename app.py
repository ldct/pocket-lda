from flask import Flask, redirect, make_response, request
import sys
import requests
from pymongo import MongoClient

app = Flask(__name__)

with open('POCKET_API_KEY') as f:
    POCKET_API_KEY = f.readlines()[0]
JSON_HEADERS = {'Content-type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}

@app.route('/')
def hello_world():

    r = requests.post('https://getpocket.com/v3/oauth/request', json={
        'consumer_key': POCKET_API_KEY,
        'redirect_uri': 'http://107.170.195.93/rcv_oauth'
    }, headers=JSON_HEADERS)

    request_token = r.json()['code']

    redirect_url = ''
    redirect_url += 'https://getpocket.com/auth/authorize'
    redirect_url += '?request_token=' + request_token
    redirect_url += '&redirect_uri=' + 'http://107.170.195.93/rcv_oauth'

    response = make_response(redirect(redirect_url))
    response.set_cookie('request_token', request_token)

    return response

@app.route('/rcv_oauth')
def receive_oauth():

    request_token = request.cookies.get('request_token')
    print('request_token', request_token)

    r = requests.post('https://getpocket.com/v3/oauth/authorize', json={
        'consumer_key': POCKET_API_KEY,
        'code': request_token
    }, headers=JSON_HEADERS)

    access_token = r.json()['access_token']
    username = r.json()['username']

    r = requests.post('https://getpocket.com/v3/get', json={
        'consumer_key': POCKET_API_KEY,
        'access_token': access_token,
        'state': 'all',
        'count': 5,
        'detailType': 'simple'
    }, headers=JSON_HEADERS)

    resolved_urls = [item['resolved_url'] for item in r.json()['list'].values()]
    print(resolved_urls)



    return 'oauth redirect'

port = int(sys.argv[1]) or 5000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)