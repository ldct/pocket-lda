from flask import Flask
import sys

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

port = int(sys.argv[1]) or 5000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)