from flask import Flask, request, jsonify
import json, requests
import subprocess, socket, os
from nacl import secret
from nacl.encoding import Base64Encoder

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    print(data)
    if data["token"] == "":
        return jsonify({'auth': 'fail', 'token': ''})
   
    key = b'\xa0K\x89w\xa9\xe6\xed\xdb\xa4\xacj\xec\xbb\x16Q\x82\x96\n|i\x95^?0\x1b/\xb22x\x13\xdb\x0e'
    box = secret.SecretBox(key)
    
    try:
        decrypted_token = box.decrypt(data['token'].encode(), encoder=Base64Encoder)
        return jsonify({'auth': 'success', 'token': decrypted_token})
    except:
        return jsonify({'auth': 'fail', 'token': ''})
    
def run():
    app.run(host='127.0.0.1', port=5001, debug=True)

def main():
    run()

if __name__ == "__main__":
    main()	


