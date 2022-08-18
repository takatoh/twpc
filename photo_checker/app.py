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
    photo_info = load_photo_info(CONFIG['infoFile'])
    return dict(photo_list=photo_list, photo_info=photo_info)


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


def load_photo_info(info_file):
    with open(info_file, 'r') as f:
        src_info_list = json.load(f)
    photo_info = {}
    for src_info in src_info_list:
        created_at = src_info['created_at']
        for photo in src_info['photos']:
            file_name = photo['media_url'].split('/')[-1]
            photo_info[file_name] = {
                'file_name': file_name,
                'media_url' : photo['media_url'],
                'expanded_url' : photo['expanded_url'],
                'created_at' : created_at
            }
    return photo_info
