import tweepy


class TweetedPhotoDownloader():
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        self._api = tweepy.API(auth)
        self.result = None

    def get_by_id(self, tweet_id):
        self.result = None
        status = self._api.get_status(tweet_id)
        if 'extended_entities' in status._json and 'media' in status._json['extended_entities']:
            entities = status._json['extended_entities']
        elif 'entities' in status._json and 'media' in status._json['entities']:
            entities = status._json['entities']
        else:
            return self.result
        self.result = {
            'screen_name' : status.user.screen_name,
            'created_at' : status.created_at,
            'id' : status.id,
            'photos' : []
        }
        for media in entities['media']:
            if media['type'] == 'photo':
                sizes = {}
                for k, v in media['sizes'].items():
                    sizes[k] = {
                        'w' : v['w'],
                        'h' : v['h'],
                        'resize' : v['resize']
                    }
                self.result['photos'].append({
                    'media_url' : media['media_url_https'],
                    'expanded_url' : media['expanded_url'],
                    'sizes' : sizes
                })
        return self.result
