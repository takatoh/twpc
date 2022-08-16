import tweepy
import json
import os
import requests
import argparse
from pprint import pprint
from get_tweeted_photo import __version__, TweetedPhotoDownloader

SCRIPT_VERSION = f'v{__version__}'
CONFIG_FILE_NAME = '.tweepy_config.json'


def main():
    args = parse_arguments()

    config = load_config()

    downloader = TweetedPhotoDownloader(
        config['consumer_key'],
        config['consumer_secret'],
        config['access_token_key'],
        config['access_token_secret']
    )

    if args.id:
        result = downloader.get_by_id(args.id)
        if result is None:
            print('No media')
            exit(0)
        screen_name = result['screen_name']
        created_at = result['created_at']
        tweet_id = result['id']
        print(f'@{screen_name} at {created_at}(id={tweet_id}')
        for photo in result['photos']:
            media_url = photo['media_url']
            expanded_url = photo['expanded_url']
            print(f'  media url: {media_url}')
            print(f'  expanded url: {expanded_url}')
            if args.size:
                for k, v in photo['sizes'].items():
                    w = v['w']
                    h = v['h']
                    resize = v['resize']
                    print(f'    {k}: {w}x{h} ({resize})')
            if args.download:
                res = requests.get(media_url)
                os.makedirs(args.download, exist_ok=True)
                file_name = os.path.join(args.download, media_url.split('/')[-1])
                with open(file_name, 'wb') as f:
                    f.write(res.content)
        exit(0)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'{SCRIPT_VERSION}'
    )
    parser.add_argument(
        '-i', '--id',
        action='store',
        type=int,
        metavar='TWEET_ID',
        help='specify tweet ID'
    )
    parser.add_argument(
        '-d', '--download',
        action='store',
        metavar='DIR',
        default='.',
        help='download photos into DIR'
    )
    parser.add_argument(
        '-s', '--size',
        action='store_true',
        help='display photo sizes'
    )
    args = parser.parse_args()
    return args


def load_config():
    config_file = os.path.join(os.environ['HOME'], CONFIG_FILE_NAME)
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config
