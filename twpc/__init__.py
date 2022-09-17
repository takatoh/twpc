import os
import json


__version__ = '0.9.0'

CONFIG_FILE_NAME = '.twpc-config.json'


def load_config(config_file=None):
    config_file = config_file or os.path.join(os.environ['HOME'], CONFIG_FILE_NAME)
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config
