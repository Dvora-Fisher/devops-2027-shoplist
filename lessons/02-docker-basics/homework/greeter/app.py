# Greeter: a tiny web service for the lesson 2 homework.
# Reads the greeting from an environment variable, like the ShopList backend.
import os
from flask import Flask, jsonify

app = Flask(__name__)
GREETING = os.environ.get('GREETING', 'Hello')


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/hello/<name>')
def hello(name):
    return jsonify({'message': f'{GREETING}, {name}!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
