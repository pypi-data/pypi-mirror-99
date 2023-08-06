import json
import sys
from base64 import b64encode
from http.client import HTTPSConnection

from halo import Halo
from log_symbols import LogSymbols

from .config import get_config


def show_usage():
    print("Usage:\n\tCreate log: lbk @context")


def add_log(context):
    server_url, username, password = get_config()

    message = ''
    line = input('> ')
    while len(line) > 0:
        message += line
        line = input('> ')

    spinner = Halo(text='Sending', spinner='bouncingBall', color='white')
    spinner.start()

    credentials = bytes(f"{username}:{password}", encoding='UTF-8')
    user_and_pass = b64encode(credentials).decode("ascii")
    headers = {
        'Authorization': f'Basic {user_and_pass}',
        'Content-Type': 'application/json'
    }

    body = json.dumps({
        'context': context,
        'message': message
    })

    conn = HTTPSConnection(server_url)
    conn.request('POST', '/api/logs', body, headers=headers)
    response = conn.getresponse()
    if response.status == 200:
        spinner.stop_and_persist(symbol=LogSymbols.SUCCESS.value, text='Ok')
    else:
        spinner.stop_and_persist(symbol=LogSymbols.ERROR.value, text='Failed')
        print(f'Response status {response.status}')


def main():
    if len(sys.argv) > 1:
        if sys.argv[1][0] == '@':
            add_log(sys.argv[1])
        else:
            show_usage()
    else:
        show_usage()


if __name__ == '__main__':
    main()
