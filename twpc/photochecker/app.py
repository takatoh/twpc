from bottle import route, redirect, view, static_file, run, TEMPLATE_PATH
import requests
from pathlib import Path
import os
import json
from twpc import load_config
from .photo_info_handler import PhotoInfoHandler


DEFAULT_PORT = 8080
CONFIG = load_config()
TEMPLATE_PATH.append(Path(__file__).parent / 'views')
STATIC_FILE_DIR = str(Path(__file__).parent / 'static_files')


@route('/')
@view('index')
def index():
    photo_list = list_photo_files(CONFIG['photoDir'])
    photo_info = load_photo_info(CONFIG['infoFile'])
    photo_list = [ photo for photo in photo_list if str(photo.name) in photo_info ]
    photo_list.sort(key=lambda itm: photo_info[itm.name]['status_id'])
    photo_count = len(photo_list)
    return dict(photo_list=photo_list, photo_info=photo_info, photo_count=photo_count)


@route('/images/<filepath:path>')
def send_iamge(filepath):
    return static_file(filepath, root=CONFIG['photoDir'])


@route('/statics/<filepath:path>')
def send_static_file(filepath):
    return static_file(filepath, root=STATIC_FILE_DIR)


@route('/delete/<filename>')
def delete_photo(filename):
    delete_photo_file(filename, CONFIG['photoDir'])
    delete_photo_info(filename, CONFIG['infoFile'])
    return redirect('/')


@route('/post/<filename>')
@view('post_complete')
def post_photo(filename):
    filepath = Path(CONFIG['photoDir']) / filename
    photo_info = load_photo_info(CONFIG['infoFile'])[filename]
    src_url = photo_info['media_url'] + '?name=large'
    data = {
        'url' : src_url,
        'page_url' : '',
        'tags' : '',
        'add_tags' : False
    }
    server_url = CONFIG['sombreroHostUrl'].rstrip('/') + '/api/post'
    with open(filepath, 'rb') as f:
        files = {
            'file' : (filename, f)
        }
        res = requests.post(server_url, data=data, files=files)
    if res.status_code == requests.codes.ok:
        res_data = res.json()
        status = res_data['status']
        if status == 'Accepted':
            message = 'The file has been accepted.'
        elif status == 'Rejected':
            reason = res_data['reason']
            message = f'The file has been rejected for the reason: {reason}.'
    else:
        status = 'Error!'
        message = f'Error occured: code = {res.status_code}'
    return dict(status=status, message=message, filename=filename)


def run_server(port=DEFAULT_PORT):
    run(host='localhost', port=port, debug=True)


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


def delete_photo_file(filename, directory):
    base_dir = Path(directory)
    (base_dir / filename).unlink()
    (base_dir / 'thumbs' / filename).unlink()


def delete_photo_info(filename, info_file):
    handler = PhotoInfoHandler(info_file)
    handler.delete(filename)
