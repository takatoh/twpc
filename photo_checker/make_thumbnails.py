from PIL import Image
from pathlib import Path
import argparse

THUMBNAIL_DIR = 'thumbs'
THUMBNAIL_GEOMETRY = (180, 180)


def main():
    args = parse_arguments()

    src_dir = Path(args.dir)
    thumbs_dir = src_dir / THUMBNAIL_DIR
    thumbs_dir.mkdir(exist_ok=True)

    for src in src_dir.iterdir():
        if not (src.is_file() and src.suffix in ['.png', '.jpg', '.jpeg']):
            continue
        thumb = thumbs_dir / src.name
        if thumb.exists():
            continue
        make_thumbnail(src, thumb)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dir',
        action='store',
        metavar='DIR',
        help='original image'
    )
    args = parser.parse_args()
    return args


def make_thumbnail(src_file, thumb_file):
    img = Image.open(src_file, 'r')
    img.thumbnail(THUMBNAIL_GEOMETRY, Image.ANTIALIAS)
    img.save(thumb_file)
