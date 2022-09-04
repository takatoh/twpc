import json
import os
import argparse
from pprint import pprint
from . import __version__, TweetedPhotoDownloader, JSONWithDateTimeEncoder

SCRIPT_VERSION = f'v{__version__}'
CONFIG_FILE_NAME = '.twpc-config.json'


def main():
    args = parse_arguments()

    config = load_config()

    downloader = TweetedPhotoDownloader(
        config['consumerKey'],
        config['consumerSecret'],
        config['accessTokenKey'],
        config['accessTokenSecret']
    )

    if args.id:
        result = downloader.get_by_id(args.id)
    elif args.user:
        result = downloader.get_by_username(args.user)
    elif args.user_list:
        with open(args.user_list, 'r') as f:
            user_list = [ u for u in [ l.strip() for l in f.readlines() ] if u ]
        result = downloader.get_by_userlist(user_list)

    if result is None:
        print('No media')
        exit(0)
    if args.log:
        log = open_log(args.log)
        ids = [ t['id'] for t in log ]
        for tweet in result:
            if not tweet['id'] in ids:
                log.append(tweet)
        save_log(log, args.log)
    elif args.dump:
        print(dump_as_json(result))
    else:
        for tweet in result:
            print_tweet(tweet, args.size)

    if args.download:
        download_dir = args.download
        os.makedirs(download_dir, exist_ok=True)
        count = downloader.download_all(download_dir)
        print(f'{count} photos downloaded')

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
        '-u', '--user',
        action='store',
        default=None,
        help='specify user(screen_name)'
    )
    parser.add_argument(
        '-U', '--user-list',
        action='store',
        metavar='FILE',
        default=None,
        help='read user list from FILE'
    )
    parser.add_argument(
        '-d', '--download',
        action='store',
        metavar='DIR',
        default=None,
        help='download photos into DIR'
    )
    parser.add_argument(
        '-D', '--dump',
        action='store_true',
        help='dump as JSON'
    )
    parser.add_argument(
        '-l', '--log',
        action='store',
        metavar='FILE',
        default=None,
        help='output log as JSON to FILE'
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


def print_tweet(tweet, size=False):
    screen_name, created_at, tweet_id = tweet['screen_name'], tweet['created_at'], tweet['id']
    print(f'@{screen_name} at {created_at}(id={tweet_id}')
    for photo in tweet['photos']:
        media_url, expanded_url = photo['media_url'], photo['expanded_url']
        print(f'  media url: {media_url}')
        print(f'  expanded url: {expanded_url}')
        if size:
            for k, v in photo['sizes'].items():
                w, h, resize = v['w'], v['h'], v['resize']
                print(f'    {k}: {w}x{h} ({resize})')


def dump_as_json(tweets):
    return json.dumps(tweets, indent=2, ensure_ascii=False, cls=JSONWithDateTimeEncoder)


def open_log(logfile):
    if os.path.exists(logfile):
        with open(logfile, 'r') as f:
            log = json.load(f)
    else:
        log = []
    return log


def save_log(log, logfile):
    with open(logfile, 'w') as f:
        f.write(dump_as_json(log))
