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

    oauth_provider = oauth_consts.URL + ":" + oauth_consts.PORT + '/login'
    headers = {'Content-Type': 'application/json'}
    #data = {'username': username, 'password': password}
    data = {"grant_type": "client_credentials","username": username,"password": password}
    parsed_data = json.dumps(data)

    response = requests.post(oauth_provider, headers=headers, data=parsed_data)
    auth_status = response.json()['auth']
    token = response.json()['token']

    # Uncomment below and comment out 3 lines 
    # above for testing without O-Auth provider
    
    # auth_status = 'success'
    # token = 'abc123'

    h = sha3.sha3_256(password.encode())
    hashed_password = h.digest()

    if auth_status == 'success' and token != '':
        # TODO: insert crypto

        return jsonify({'auth': 'success', 'token': token})
    else:
        return jsonify({'auth': 'fail', 'token': ''})

def main():
    #app.run(host=auth_consts.FLASK_HOST, port=auth_consts.FLASK_PORT)
    app.run()

if __name__ == '__main__':
    main()
