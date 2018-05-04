import requests, json

def bad_token_test():
    headers = {'Content-Type' : 'application/json'}
    data = {'token': 'fail',}
    r = requests.post('http://127.0.0.1:5001', data=json.dumps(data), headers=headers)

    print(r.text)

def main():
    bad_token_test()

main()
