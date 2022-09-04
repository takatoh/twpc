from PIL import Image
from pathlib import Path
import json
import os
import argparse

THUMBNAIL_DIR = 'thumbs'
THUMBNAIL_GEOMETRY = (180, 180)
IMAGE_SUFFIXES = ['.png', '.jpg', '.jpeg']
config_file = os.environ.get('HOME') + '/.twpc-config.json'
with open(config_file, 'r') as f:
    CONFIG = json.load(f)


def main():
    args = parse_arguments()

    src_dir = Path(args.dir or CONFIG['photoDir'])
    thumbs_dir = src_dir / THUMBNAIL_DIR

    count = make_thumbnails(src_dir, thumbs_dir, verbose=args.verbose)
    if args.verbose:
        print(f'\n{count} thumbnails are made')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dir',
        action='store',
        metavar='DIR',
        nargs='?',
        default=None,
        help='specify original photo DIR, or from configuration file'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='verbose mode'
    )
    args = parser.parse_args()
    return args


def make_thumbnails(src_dir, thumbs_dir, verbose=False):
    src_dir, thumbs_dir = Path(src_dir), Path(thumbs_dir)
    thumbs_dir.mkdir(exist_ok=True)

    count = 0
    for src in src_dir.iterdir():
        if not (src.is_file() and src.suffix in IMAGE_SUFFIXES):
            continue
        thumb = thumbs_dir / src.name
        if thumb.exists():
            continue
        if verbose:
            print(f'{src}')
            print(f'  => {thumb}')
        make_thumbnail(src, thumb)
        count += 1
    return count


def make_thumbnail(src_file, thumb_file):
    img = Image.open(src_file, 'r')
    img.thumbnail(THUMBNAIL_GEOMETRY, Image.ANTIALIAS)
    img.save(thumb_file)
