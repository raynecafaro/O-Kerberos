import os

# Enter in Flask APP information
class AUTHServerConfig(object):
    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 80
    KEY = b'\xa0K\x89w\xa9\xe6\xed\xdb\xa4\xacj\xec\xbb\x16Q\x82\x96\n|i\x95^?0\x1b/\xb22x\x13\xdb\x0e'

    def __init__(self):
        self.FLASK_HOST = FLASK_HOST
        self.FLASK_PORT = FLASK_PORT
        self.KEY = KEY

# Enter in destination OAUTH Provider Information
class OAUTHConfig(object):
    
    URL = "http://127.0.0.1"
    PORT = "80"

    def __init__(self):
        self.URL = URL
        self.PORT = PORT
