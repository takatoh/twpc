from bottle import route, run
from pathlib import Path


@route('/hello')
def hello():
    return 'Hello, World!'


@route('/photos')
def photos():
    photos = list_photo_files('/home/takatoh/w/photo-checker/photos')
#    return str(photos)
    html = '''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Photos</title>
  </head>
  <body>
    <h1>Photos</h1>
    <ul>
'''
    for photo in photos:
        html += f'      <li>{photo.name}</li>\n'
    html += '''    </ul>
  </body>
</html>
'''
    return html


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
