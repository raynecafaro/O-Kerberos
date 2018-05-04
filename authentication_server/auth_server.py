from flask import Flask, jsonify, request
import requests
import json
import sha3
import libnacl
from nacl import secret
from nacl.encoding import Base64Encoder
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
    data = {"grant_type": "client_credentials","client_id": username,"client_secret": password}
    parsed_data = json.dumps(data)

    response = requests.post(oauth_provider, headers=headers, data=parsed_data)
    token = response.json()['access_token']

    if requests.codes.ok == response.status_code and token != '':
        box = secret.SecretBox(auth_consts.KEY)
        ct = box.encrypt(token.encode(), encoder=Base64Encoder)
        json_response = {'auth': 'success', 'token': ct.decode()}
        
        h = sha3.sha3_256(password.encode())
        password_box = secret.SecretBox(h.digest())
        encrypted_json = password_box.encrypt(json.dumps(json_response)).encode(), encoder=Base64Encoder)

        return jsonify({'response': encrypted_message})
    else:
        return jsonify({'auth': 'fail', 'token': ''})

def main():
    #app.run(host=auth_consts.FLASK_HOST, port=auth_consts.FLASK_PORT)
    app.run()

if __name__ == '__main__':
    main()
