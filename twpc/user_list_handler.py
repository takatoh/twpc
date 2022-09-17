import json


class UserListHandler:
    def __init__(self,list_file):
        self.list_file = list_file
        self._load()

    def add(self, user):
        user = user.strip('@')
        if user in self.list:
            raise UserExist(user)
        self.list.append(user)
        self._save()
        return user

    def remove(self, user):
        user = user.strip('@')
        if not user in self.list:
            raise UserNotFound(user)
        self.list.remove(user)
        self._save()
        return user

    def _load(self):
        with open(self.list_file, 'r') as f:
            self.list = [ u for u in [ l.strip() for l in f.readlines() ] if u ]

    def _save(self):
        with open(self.list_file, 'w') as f:
            f.write('\n'.join(self.list))


class UserExist(Exception):
    pass


class UserNotFound(Exception):
    pass
