from ._base_import import *


def cmd_wop(message):
    s = ''
    print("Wop msg", message)
    if 'fwd_messages' in message:
        for text in message['fwd_messages']:
            s += ''.join(map(lambda x: keys_wop[x] if x in keys_wop else x, text['body']))
        return "@!\n%s\n©[id%s|%s]" % (s, message['uid'], api.users.get(**{'user_ids': message['uid']})[0]['first_name'])
    return '@!Нет сообщений для "wop"!'