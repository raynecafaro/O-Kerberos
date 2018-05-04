from flask import Flask, jsonify, request
import requests
import json
import sha3
import libnacl
from config_constants import OAUTHConfig as oauth_consts
from config_constants import AUTHServerConfig as auth_consts

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    username = credentials['username']
    password = credentials['password']

    if username == '' or password == '':
        return jsonify({'auth': 'fail', 'token': ''})

    oauth_provider = oauth_consts.URL + ":" + oauth_consts.PORT + '/token.php'
    headers = {'Content-Type': 'application/json'}
    data = {"grant_type": "client_credentials","username": username,"password": password}
    parsed_data = json.dumps(data)

    response = requests.post(oauth_provider, headers=headers, data=parsed_data)
    token = response.json()['access_token']

    #h = sha3.sha3_256(password.encode())
    #hashed_password = h.digest()

    if response.status_code == r.status_code and token != '':
        # TODO: insert crypto

        return jsonify({'auth': 'success', 'token': token})
    else:
        return jsonify({'auth': 'fail', 'token': ''})

def main():
    #app.run(host=auth_consts.FLASK_HOST, port=auth_consts.FLASK_PORT)
    app.run()

if __name__ == '__main__':
    main()
