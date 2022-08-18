from bottle import route, view, static_file, run, TEMPLATE_PATH
from pathlib import Path
import os
import json
from photo_checker.photo_info_handler import PhotoInfoHandler


config_file = os.environ.get('HOME') + '/photo-checker-config.json'
with open(config_file, 'r') as f:
    CONFIG = json.load(f)
TEMPLATE_PATH.append(Path(__file__).parent / 'views')
STATIC_FILE_DIR = str(Path(__file__).parent / 'static_files')


@route('/')
@view('index')
def index():
    photo_list = list_photo_files(CONFIG['photoDir'])
    photo_info = load_photo_info(CONFIG['infoFile'])
    photo_list.sort(key=lambda itm: photo_info[itm.name]['status_id'])
    return dict(photo_list=photo_list, photo_info=photo_info)


@route('/images/<filepath:path>')
def send_iamge(filepath):
    return static_file(filepath, root=CONFIG['photoDir'])


@route('/statics/<filepath:path>')
def send_static_file(filepath):
    return static_file(filepath, root=STATIC_FILE_DIR)


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
    handler = PhotoInfoHandler(info_file)
    photo_info = handler.convert()
    return photo_info
