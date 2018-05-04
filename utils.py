from nacl import utils
from nacl import secret

def key_gen():
    return utils.random(secret.SecretBox.KEY_SIZE)

def main():
    print(key_gen())

if __name__ == '__main__':
    main()
