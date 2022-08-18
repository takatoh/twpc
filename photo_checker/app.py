from bottle import route, view, static_file, run, TEMPLATE_PATH
from pathlib import Path
import os
import json


config_file = os.environ.get('HOME') + '/photo-checker-config.json'
with open(config_file, 'r') as f:
    CONFIG = json.load(f)
TEMPLATE_PATH.append(Path(__file__).parent / 'views')


@route('/')
@view('index')
def index():
    photo_list = list_photo_files(CONFIG['photoDir'])
    return dict(photo_list=photo_list)


@route('/images/<filepath:path>')
def send_iamge(filepath):
    return static_file(filepath, root=CONFIG['photoDir'])


def run_server():
    run(host='localhost', port=8080, debug=True)


def list_photo_files(directory):
    base_dir = Path(directory)
    photo_files = []
    for file in base_dir.iterdir():
        if not (file.is_file() and file.suffix in ['.png', '.jpg', '.jpeg']):
            continue
        photo_files.append(file)
    return photo_files
