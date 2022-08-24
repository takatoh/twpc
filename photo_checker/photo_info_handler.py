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
            screen_name = info['screen_name']
            for photo in info['photos']:
                file_name = photo['media_url'].split('/')[-1]
                photo_info[file_name] = {
                    'file_name': file_name,
                    'status_id' : status_id,
                    'media_url' : photo['media_url'],
                    'expanded_url' : photo['expanded_url'],
                    'created_at' : created_at,
                    'screen_name' : screen_name
                }
        return photo_info

    def _load(self):
        with open(self.info_file, 'r') as f:
            self.info_list = json.load(f)

    def _save(self):
        with open(self.info_file, 'w') as f:
            json.dump(self.info_list, f, ensure_ascii=False, indent=2)

    def delete(self, filename):
        for info in self.info_list:
            del_idx = -1
            for i, photo in enumerate(info['photos']):
                photo_file_name = photo['media_url'].split('/')[-1]
                if filename == photo_file_name:
                    del_idx = i
                    break
            if del_idx >= 0:
                info['photos'].pop(del_idx)
        self._save()
