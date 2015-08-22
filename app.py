from flask import Flask, redirect, make_response, request
import sys
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

app = Flask(__name__)

with open('POCKET_API_KEY') as f:
    POCKET_API_KEY = f.readlines()[0]

with open('MONGOLAB_PASSWORD') as f:
    MONGOLAB_PASSWORD = f.readlines()[0]

connection = MongoClient("ds033153.mongolab.com", 33153)
db = connection["pocket-dla"]
db.authenticate("xuanji", MONGOLAB_PASSWORD)

mongo_ru = db.resolved_urls
mongo_texts = db.texts

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

    if (mongo_ru.count({
        'username': username,
    })):
        return 'already added'

    r = requests.post('https://getpocket.com/v3/get', json={
        'consumer_key': POCKET_API_KEY,
        'access_token': access_token,
        'state': 'all',
        'detailType': 'simple'
    }, headers=JSON_HEADERS)

    resolved_urls = [item['resolved_url'] for item in r.json()['list'].values()]

    mongo_ru.insert({
        'username': username,
        'resolved_urls': resolved_urls,
    })

    mongo_texts.insert([{
        'resolved_url': url
    } for url in resolved_urls])

    return 'added'

def resolve(url):

    print('resolve', url)

    text_url = ''
    text_url += 'http://text.readitlater.com/v3beta/text'
    text_url += '?images=0&output=json&msg=1'
    text_url += '&url=' + url

    r = requests.get(text_url)

    html = r.json()['article']

    if (html == False):
        return ''

    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

@app.route('/work-on-texts')
def work_on_text():

    naked_texts = mongo_texts.find({
        'article': None,
    }, limit=5)

    for naked_text in naked_texts:
        url = naked_text['resolved_url']
        _id = naked_text['_id']

        print(_id)

        mongo_texts.update({
            'resolved_url': url,
        }, {
            '$set': {
                'article': resolve(url)
            }
        })

    return str(mongo_texts.count({
        'article': None,
    }))


port = int(sys.argv[1])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)