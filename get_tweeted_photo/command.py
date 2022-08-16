import tweepy
import json
import os
import argparse
from pprint import pprint
from get_tweeted_photo import __version__

SCRIPT_VERSION = __version__
CONFIG_FILE_NAME = '.tweepy_config.json'


def main():
    args = parse_arguments()

    config = load_config()

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token_key'], config['access_token_secret'])
    api = tweepy.API(auth)

    if args.id:
        status =api.get_status(args.id)
        for k, v in status._json.items():
            print(k)
        if 'media' not in status.entities:
            print('No media')
            exit(0)
        print(f'@{status.user.screen_name} at {status.created_at}(id={status.id})')
        print(len(status._json['extended_entities']['media']))
        for media in status._json['extended_entities']['media']:
            if media['type'] == 'photo':
                media_url = media['media_url_https']
                expanded_url = media['expanded_url']
                print(f'  media: {media_url}')
                print(f'  expanded url: {expanded_url}')
        exit(0)

    if args.json:
        status =api.get_status(args.json)
        if status._json:
            print(True)
            if 'extended_entities' in status._json:
                print('extended_entities')
                if 'media' in status._json['extended_entities']:
                    print('extended_entities.media')
            if 'entities' in status._json:
                print('entities')
                if 'media' in status._json['entities']:
                    print('entities.media')
        else:
            print(False)
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
        '-j', '--json',
        action='store',
        type=int,
        help='display json'
    )
    args = parser.parse_args()
    return args


def load_config():
    config_file = os.path.join(os.environ['HOME'], CONFIG_FILE_NAME)
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config
