from . import __version__, CONFIG_FILE_NAME, load_config
import os
import json
from pathlib import Path
from pprint import pprint
from .tweetedphoto import Downloader, JSONWithDateTimeEncoder
from .photochecker.thumbnail import make_thumbnail, make_thumbnails, THUMBNAIL_DIR
from .photochecker.app import run_server
import click


def main():
    cmd(obj={})


@click.group()
@click.pass_context
@click.version_option(version=__version__, message='v%(version)s')
def cmd(ctx):
    pass


@cmd.command(help='Get tweeted photos.')
@click.pass_context
def get(ctx):
    config = load_config()

    downloader = Downloader(
        config['consumerKey'],
        config['consumerSecret'],
        config['accessTokenKey'],
        config['accessTokenSecret']
    )

    user_list = config['userList']
    with open(user_list, 'r') as f:
        user_list = [ u for u in [ l.strip() for l in f.readlines() ] if u ]
    result = downloader.get_by_userlist(user_list)

    if result is None:
        print('No media')
        exit(0)

    logfile = config['infoFile']
    log = open_log(logfile)
    ids = [ t['id'] for t in log ]
    tweets = [ tweet for tweet in result if not tweet['id'] in ids ]
    log.extend(tweets)
    save_log(log, logfile)

    download_dir = config['photoDir']
    os.makedirs(download_dir, exist_ok=True)
    count = downloader.download(download_dir, tweets)
    print(f'{count} photos downloaded')


@cmd.command(help='Make thumbnails.')
@click.pass_context
@click.option('--verbose', '-v', is_flag=True, help='Verbose mode.')
def mkthumbs(ctx, verbose):
    config = load_config()
    src_dir = Path(config['photoDir'])
    thumbs_dir = src_dir / THUMBNAIL_DIR

    count = make_thumbnails(src_dir, thumbs_dir, verbose=verbose)
    if verbose:
        print(f'\n{count} thumbnails are made.')


@cmd.command(help='Run server.')
@click.pass_context
@click.option('--port', '-p', type=int, default=8080, help='specify port.')
def serve(ctx, port):
    config = load_config()
    src_dir = Path(config['photoDir'])
    thumbs_dir = src_dir / THUMBNAIL_DIR
    print('Making thumbnails...')
    count = make_thumbnails(src_dir, thumbs_dir)
    run_server(port=port)


@cmd.command(help='Handle user list.')
@click.pass_context
@click.option('--list', '-l', is_flag=True, help='List users.')
@click.option('--add', '-a', metavar='USER', help='Add user')
def user(ctx, list, add):
    config = load_config()
    with open(config['userList'], 'r') as f:
        user_list = [ u for u in [ l.strip() for l in f.readlines() ] if u ]
    if list:
        for user in user_list:
            print(user)
    elif add:
        user = add.strip('@')
        if user in user_list:
            print(f'Already exist: {user}')
            exit(0)
        else:
            user_list.append(user)
            with open(config['userList'], 'w') as f:
                f.write('\n'.join(user_list))
            print(f'Added user: {user}')


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
