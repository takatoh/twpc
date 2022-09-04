from . import __version__
import os
import json
from pprint import pprint
from .tweetedphoto import TweetedPhotoDownloader, JSONWithDateTimeEncoder
import click

CONFIG_FILE_NAME = '.twpc-config.json'


def main():
    cmd(obj={})


@click.group()
@click.pass_context
@click.version_option(version=__version__, message='v%(version)s')
def cmd(ctx):
    pass


@cmd.command(help='Get tweeted photos.')
@click.pass_context
@click.option('--id', '-i', 'tweet_id', type=int, help='specify tweet ID.')
@click.option('--user', '-u', help='specify user(screen_name).')
@click.option('--user-list', '-U', help='read user list from FILE.')
@click.option('--download', '-d', help='download photos into DIR.')
@click.option('--dump', '-D', is_flag=True, help='dump as JSON.')
@click.option('--log', '-l', help='output log as JSON to FILE.')
@click.option('--size', '-s', is_flag=True, help='display photo sizes.')
def get(ctx, tweet_id, user, user_list, download, dump, log, size):
    config = load_config()

    downloader = TweetedPhotoDownloader(
        config['consumerKey'],
        config['consumerSecret'],
        config['accessTokenKey'],
        config['accessTokenSecret']
    )

    if tweet_id:
        result = downloader.get_by_id(tweet_id)
    elif user:
        result = downloader.get_by_username(user)
    elif user_list:
        with open(user_list, 'r') as f:
            user_list = [ u for u in [ l.strip() for l in f.readlines() ] if u ]
        result = downloader.get_by_userlist(user_list)

    if result is None:
        print('No media')
        exit(0)
    if log:
        log = open_log(log)
        ids = [ t['id'] for t in log ]
        for tweet in result:
            if not tweet['id'] in ids:
                log.append(tweet)
        save_log(log, log)
    elif dump:
        print(dump_as_json(result))
    else:
        for tweet in result:
            print_tweet(tweet, size)

    if download:
        download_dir = download
        os.makedirs(download_dir, exist_ok=True)
        count = downloader.download_all(download_dir)
        print(f'{count} photos downloaded')

    exit(0)



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
