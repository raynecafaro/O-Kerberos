import argparse
import requests, json

def arguments():
    parser = argparse.ArgumentParser(description='O-Kerberos Client')

    parser.add_argument("-c", "--connect", action="store", type=str)
    parser.add_argument("-u", "--username", action="store", type=str)
    parser.add_argument("-p", "--password", action="store", type=str)
    
    args = parser.parse_args()

    return args

def connect(args):
    headers = {'Content-Type' : 'application/json'}
    data = {'username': args.username, 'password': args.password}
    parsed_data = json.dumps(data)
    
    r = requests.post(args.connect,  headers=headers, data=parsed_data)

    print(r.text)

def main():
    args = arguments() 
    connect(args)

if __name__ ==  "__main__":
    main()
