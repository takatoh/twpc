import json


class PhotoInfoHandler():
    def __init__(self, info_file):
        self.info_file = info_file
        self._load()

    def convert(self):
        photo_info = {}
        for info in self.info_list:
            status_id = info['id']
            created_at = info['created_at']
            for photo in info['photos']:
                file_name = photo['media_url'].split('/')[-1]
                photo_info[file_name] = {
                    'file_name': file_name,
                    'status_id' : status_id,
                    'media_url' : photo['media_url'],
                    'expanded_url' : photo['expanded_url'],
                    'created_at' : created_at
                }
        return photo_info

    def _load(self):
        with open(self.info_file, 'r') as f:
            self.info_list = json.load(f)
