from flask import Flask, jsonify, request
import requests
import json
import hashlib
import libnacl
import base64
from nacl import secret
from nacl.encoding import Base64Encoder
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from config_constants import OAUTHConfig as oauth_consts
from config_constants import AUTHServerConfig as auth_consts

app = Flask(__name__)

def decrypt_creds(data):
    with open("./private.pem") as f:
        key_text = f.read()

    privkey = RSA.importKey(key_text)

    cipher = PKCS1_v1_5.new(privkey)

    ct = base64.b64decode(data)

    pt = cipher.decrypt(ct, None)
    
    print(pt.decode())
    return json.loads(pt.decode())
    

@app.route('/login', methods=['POST'])
def login():
    #credentials = request.get_json()
    encrypted_credentials = request.get_data()
    
    credentials = decrypt_creds(encrypted_credentials)
    
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
    print(response.text)

    if requests.codes.ok == response.status_code and token != '':
        box = secret.SecretBox(auth_consts.KEY)
        ct = box.encrypt(token.encode(), encoder=Base64Encoder)
        json_response = {'auth': 'success', 'token': ct.decode()}
        print(json_response)
 
        h = hashlib.sha256(password.encode())
        password_box = secret.SecretBox(h.digest())
        encrypted_json = password_box.encrypt(json.dumps(json_response).encode(), encoder=Base64Encoder)
        print(encrypted_json)

        return jsonify({'response': encrypted_json.decode()})
    else:
        return jsonify({'auth': 'fail', 'token': ''})

def main():
    #app.run(host=auth_consts.FLASK_HOST, port=auth_consts.FLASK_PORT)
    app.run()

if __name__ == '__main__':
    main()
