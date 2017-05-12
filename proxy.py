import os
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


USERFEEDS_API_KEY = os.environ['USERFEEDS_API_KEY']
USERFEEDS_API_URL = os.environ.get('USERFEEDS_API_URL', 'https://api.userfeeds.io/beta')
DOMAINS = [i.strip() for i in os.environ['DOMAINS'].split(',')]


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
cors = CORS(app, resources={r'*': {'origins': DOMAINS}})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    if path == '':
        return render_template('home.html')

    url = '{base}/{path}'.format(base=USERFEEDS_API_URL, path=path)
    params = dict(request.args.items())

    response = requests.get(url, params=params, headers={
        'Authorization': USERFEEDS_API_KEY
    })
    print(response)
    data = response.json()
    return jsonify(data)