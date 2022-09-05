from PIL import Image
from pathlib import Path
import json
import os
import argparse

THUMBNAIL_DIR = 'thumbs'
THUMBNAIL_GEOMETRY = (180, 180)
IMAGE_SUFFIXES = ['.png', '.jpg', '.jpeg']


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
