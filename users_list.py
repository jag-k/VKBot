import json
from create_json import create_json


class Users:
    def __init__(self, file):
        import os
        self.file = "json_files/%s.json" % file
        if not os.path.isfile(self.file):
            open(self.file, 'w').write('[]')

    def edit_file(self, file):
        self.__init__(file)

    def add_user(self, user_id, per=1):
        js = json.load(open(self.file))
        for i in range(len(js)):
            if js[i]['user_id'] == user_id:
                js[i]['permission'] = per
                create_json(self.file, js, False)
                return js
        js.append({'user_id': user_id, 'permission': per})
        create_json(self.file, js, False)
        return js

    def del_user(self, user_id):
        res = [i for i in json.load(open(self.file)) if i['user_id'] != user_id]
        create_json(self.file, res, False)
        return res

    def __iter__(self):
        return json.load(open(self.file))

    def __str__(self):
        return str(self.__iter__())

    def __call__(self, per='id'):
        js = json.load(open(self.file))
        if type(per) is str and per.lower() in ['user', 'users', 'user_id', 'uid', 'u', 'id']:
            return list(map(lambda x: x['user_id'], js))
        return list(map(lambda x: x['user_id'], filter(lambda x: x['permission'] == int(per), js)))

    def __getattr__(self, item):
        js = json.load(open(self.file))
        for i in js:
            if item == i['user_id']:
                return i['permission']
        return 0
