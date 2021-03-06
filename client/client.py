import argparse
import requests, json
import hashlib
import base64
from nacl import secret
from nacl.encoding import Base64Encoder
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def encrypt_creds(data):
    key_text = ''
    with open("./public.pem", "r") as f:
        key_text = f.read()
    
    pubkey = RSA.importKey(key_text)

    cipher = PKCS1_v1_5.new(pubkey)

    ct = cipher.encrypt(data.encode())

    ct = base64.b64encode(ct)
    
    print(ct)
    return ct

def arguments():
    parser = argparse.ArgumentParser(description='O-Kerberos Client')

    parser.add_argument("-c", "--connect", action="store", type=str)
    parser.add_argument("-a", "--appserver", action="store", type=str)
    parser.add_argument("-u", "--username", action="store", type=str)
    parser.add_argument("-p", "--password", action="store", type=str)
    
    args = parser.parse_args()

    return args

def connect(args):
    headers = {'Content-Type' : 'application/json'}
    data = {'username': args.username, 'password': args.password}
    parsed_data = json.dumps(data)
    encrypted_data = encrypt_creds(parsed_data) 
    
    r = requests.post(args.connect,  headers=headers, data=encrypted_data)
    
    if 'response' in r.json():
        return r.json()['response']

    print(r.text)
    sys.exit(1)
    

def decrypt_auth_response(response, args):
    h = hashlib.sha256(args.password.encode())
    password_box = secret.SecretBox(h.digest())
    pt_response = password_box.decrypt(response.encode(), encoder=Base64Encoder)
    data = json.loads(pt_response.decode())

    return data['token']

def send_token(token, args):
    headers = {'Content-Type' : 'application/json'}
    data = {'token': token}
    parsed_data = json.dumps(data)
    r = requests.post(args.appserver, data=parsed_data, headers=headers)
   
    print(r.text)
    return r

def main():
    args = arguments() 
    response = connect(args)
    token = decrypt_auth_response(response, args)
    send_token(token, args)

if __name__ ==  "__main__":
    main()
