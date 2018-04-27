from flask import Flask, jsonify
from flask import request
import requests
import json
import hashlib
#import libnacl
from config_constants import OAUTHConfig as oauth_consts
from config_constants import AUTHServerConfig as auth_consts

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    username = credentials['username']
    password = credentials['password']

    if username == '' or password == '':
        return{'auth': 'fail', 'token': ''}

    oauth_provider = oauth_consts.URL + ":" + oauth_consts.PORT + '/login'
    headers = {'Content-Type': 'application/json'}
    data = {'username': username, 'password': password}
    parsed_data = json.dumps(data)

    response = requests.post(oauth_provider, headers=headers, data=parsed_data)
    auth_status = response.json()['auth']
    token = response.json()['token']

    h = hashlib.sha256(password.encode('UTF-8'))
    hashed_password = h.hexdigest()

    if auth_status == 'success' and token != '':
        # TODO: insert crypto

        return{'auth': 'success', 'token': token}
    else:
        return{'auth': 'fail', 'token': ''}

def main():
    app.run(host=auth_consts.FLASK_HOST, port=auth_consts.FLASK_PORT)

if __name__ == '__main__':
    main()
