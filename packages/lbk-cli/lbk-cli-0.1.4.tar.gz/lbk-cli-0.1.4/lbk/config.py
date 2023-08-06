import os.path
from configparser import RawConfigParser
from pathlib import Path


def get_config():
    lbk_file_path = str(Path.home()) + '/.lbk'
    if os.path.exists(lbk_file_path):
        config = RawConfigParser()
        config.read(lbk_file_path)
        return config.get('DEFAULT', 'server'), config.get('DEFAULT', 'username'), config.get('DEFAULT', 'password')
    else:
        print(f'Missing configuration file at {lbk_file_path}')
        exit(1)
