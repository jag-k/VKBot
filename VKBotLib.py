import random
from pprint import pprint

import math

__author__ = "Jag_k"
import time
# from VKBotAudioMessage import *
from VKBotAPI import *
from vk.exceptions import VkAPIError
import json
from printLog import PrintLog
from users_list import Users
from color import color
import sys
from course import course, normal_case
from battery import battery


format_body_list = [
    ("<br>", "\n"),
    ("&lt;", "<"),
    ("&gt;", ">"),
]


class NoCallError(Exception):
    pass


class LastMsgID:
    def __init__(self, file):
        import os
        if not os.path.isfile(file):
            open(file, 'w').close()
        self.file = file

    def __str__(self):
        with open(self.file) as file:
            return str(file.read())

    def write(self, data):
        with open(self.file, 'w') as file:
            file.write(str(data))
        return str(self)


class JsonParameters:
    def __init__(self, name):
        self.name = name

    def __call__(self):
        return json.load(open('json_files/%s.json' % self.name))

    def __iter__(self):
        call = self()
        if type(call) is dict:
            return map(lambda x: (x, call[x]), call)
        return call

    def update(self, par):
        with open('json_files/%s.json' % self.name, 'w') as file:
            file.write(json.dumps(par, indent=4))


print_log = PrintLog()
COMMAND_START = '/'
func_off = JsonParameters('func_off')
cmds = JsonParameters('cmds')
keys_wop = JsonParameters('keys_wop')
f_cmd = JsonParameters('f_cmd')
helpcmd = open('help_cmd.txt').read()
users_list = Users('users_permission')
last_msg_id = LastMsgID('last_msg.id')


def error_log(error, print_stdout=True, tupe='normal'):
    res = color("Error", 31) + ':(%s) "%s"' % (type(error).__name__, error)
    print_log(res, print_stdout=print_stdout)
    return res


def set_activity(peer_id):
    return api.messages.setActivity(peer_id=peer_id, type='typing', v=API_VERSION)


def say_bot(text, no_bot):
    return ('' if no_bot else '[id173996641|🐩 JksBot]: ') + text


def format_body(message):
    for old, new in format_body_list:
        message['body'] = message['body'].replace(old, new)
    if 'fwd_messages' in message:
        message['fwd_messages'] = [format_body(i) for i in message['fwd_messages']]
    return message


def more_data_message(message):
    message['pid'] = message['uid']
    if message['uid'] < 0:
        message['type'] = 'group'
        message['symbol'] = '⨂'
    elif message['title']:
        message['type'] = 'chat'
        message['symbol'] = '⬤'
        message['pid'] = 2000000000 + message['chat_id']
    else:
        message['type'] = 'private'
        message['symbol'] = '◯'
    message['rid'] = int(LOGIN_DATA['me']) if message['out'] else message['uid']
    message = format_body(message)

    return message


def send_me(text, no_bot=False):
    try:
        last_msg_id.write(api.messages.send(**{'user_id': LOGIN_DATA['me'], 'message': say_bot(text, no_bot)}))
    except Exception:
        time.sleep(1.001)
        send_me(text, no_bot)


def get_course_str(full_data=False):
    current_course = course()
    l = ["Код валюты: %d; ID валюты: %s\n%d %s (%s): %f ₽" % (i['num_code'], i['id'],
                                                              i['nominal'], i['char_code'],
                                                              i['name'], i['value']) for i in current_course['course']]
    if not full_data:
        for i in range(len(l)):
            l[i] = l[i].split('\n')[1]

    text = '\n\n'.join(l)
    time = current_course['time']
    res = "Курс валют на %.2d.%.2d.%.4d %.2d:%.2d:\n\n" % (time['day'], time['month'],
                                                           time['year'], time['hour'],
                                                           time['minutes']) + text
    return '\n'.join(res.split('\n\n')) if not full_data else res


def send_back(text, message, no_bot=False, fwd=list(), **key):
    last_msg_id.write(api.messages.send(**key, **{'peer_id': message['pid'],
                                                  'message': say_bot(text, no_bot),
                                                  "forward_messages": ','.join(map(str, fwd)),
                                                  "v": 5.38}))


def print_message_info(message):
    print_log(color(message['symbol'] + '  ' + name(message['rid'], full=True), 34 if message['out'] else 32) +
              "%s:" % ('' if message['rid'] in users_list() else ' (\x1b[31mnot in user_list\x1b[0m)'),
              message['body'], print_log=False)
    print_log('   ', color(message['type'].title(), 32) + ':',
              color(name(message['pid']), 36), print_log=False)
    print_log(print_log=False)
    print_log(message, print_stdout=False)


def name(u_id, name_case="nom", full=False, try_count=0):
    """
    именительный – nom, родительный – gen, дательный – dat, винительный – acc, творительный – ins, предложный – abl.
    """
    try:
        if int(u_id) < 0:
            return api.groups.getById(group_id=-u_id)[0]['name']
        if u_id >= 2000000000:
            return api.messages.getChat(chat_id=u_id-2000000000)['title']
        data = api.users.get(**{'user_ids': u_id, 'name_case': name_case})[0]
        data = [data['first_name'], data['last_name']] if full else [data['first_name']]
    except Exception as err:
        if try_count < 3:
            return name(u_id, name_case, full, try_count + 1)
        else:
            raise SystemExit(err)
    return ' '.join(data)


def quote_edit(text, message):
    if message['out']:
        api.messages.edit(keep_forward_messages=True, keep_snippets=True, peer_id=message['pid'],
                          message_id=message['mid'], message=text)
    else:
        send_back("%s\n©[id%d|%s]" % (text, message['rid'], name(message['rid'])), message)


def relevant(message, name_case="nom", full=False):
    return '[id%s|%s]' % (int(math.fabs(message['rid'])), name(message['rid'], name_case, full))


def relevant_id(u_id, name_case="nom", full=False):
    return '[id%s|%s]' % (int(math.fabs(u_id)), name(u_id, name_case, full))


def error_time(date_time): return 'Время и дата ошибки: %s' % date_time


def cmd_wop(message):
    s = []
    message['body'] = message['body']
    if 'fwd_messages' in message:
        for text in message['fwd_messages']:
            s += [''.join(map(lambda x: keys_wop()[x] if x in keys_wop() else x,
                              text['body'].replace('<br>', '\n').replace('&amp;', '&')))]
        return "@C%s" % '\n'.join(s)
    return '@!Нет сообщений для "wop"!'


def cmd_permission(message, cmd):
    res = []
    if cmd:
        for i in cmd:
            res.append("• Уровень прав у %s: %s" % (relevant(message, name_case='ins'),
                                                    filter(lambda x: x['user_id'] == i, users_list)))


def cmd_help_show(c):
    t = "• Комманда %s:%s\n" % ('; '.join(c['names']),
                                " ⚠ НЕ РАБОТАЕТ! ⚠" if any(i in func_off() for i in c['names']) else '')
    t += "Без описания" if c['about'] is None else c['about']
    t += "\n📝 " + ("Не имеет аргументов" if c['param'] is None else c['param'])
    t += "" if c['notes'] is None else "\n⚠ Примечание: " + c['notes']
    return t


def command_help(c=None):
    if c is None:
        res = []
        for i in cmds():
            if i['show']:
                res.append(cmd_help_show(i))
        return '\n\n'.join(res)

    for i in cmds():
        if c in i['names']:
            return cmd_help_show(i)
    return "Такой команды не существует!\n• " + helpcmd


def command(cmd, message):  # 0 == break, 1 == 'complete', 2 == 'version', 3 == 'result'
    cmd[0] = cmd[0].lower()

    if cmd[0] in func_off():
        return '@!Функция "%s" отключена' % cmd[0]
        
    elif cmd[0] == 'stop' and message['uid'] in users_list(2):  # /stop
        return 'break'

    elif cmd[0] == 'id':
        u_id = message['fwd_messages'][0]['uid'] if 'fwd_messages' in message else message['rid']
        return "@!%s, Ваш ID: %d (vk.com/id%d)" % (relevant_id(u_id), u_id, u_id)  # /id

    elif cmd[0] == 'connect':
        return "@!The connection is successful!"

    elif cmd[0] == 'online':
        pass

    elif cmd[0] in ['bat', 'battery']:
        battery_info = battery('b')
        bat = battery_info['Battery'][0]
        return "@!Состояние баттареи: %s" % ', '.join(bat)

    elif cmd[0] in ['per', 'perm', 'permission']:
        return cmd_permission(message, cmd[1:])

    elif cmd[0] == 'f':
        if cmd[1:]:
            if cmd[1] in f_cmd():
                f = f_cmd()[cmd[1]]
                return '@%s%s' % (f['mode'], f['text'])

    elif cmd[0] == 'update':
        return "update"

    elif cmd[0] == "on":
        if cmd[1:]:
            func_off.update(list(set(func_off()) - set(cmd[1:])))
            return "@!Функция(и) выключенны\nСписок выключенных функций: %s" % func_off()

    elif cmd[0] == "off":
        if cmd[1:]:
            func_off.update(list(set(func_off()) | set(filter(lambda x: x.lower() != 'on', cmd[1:]))))
            return "@!Функция(и) выключенны\nСписок выключенных функций: %s" % func_off()

    elif cmd[0] == 'add':
        if cmd[1:] and cmd[1] in ['admin', 'tryId']:
            if not cmd[2:] and cmd[2].isdigit():
                eval("cmd[1].update(%s)" % list(set(eval(cmd[1])) | set([cmd[2]])))
                return "@!Список \"%s\" изменён" % cmd[1]

    elif cmd[0].lower() in ['a', 'а']:
        return "@N%s" % ('ао' * int(cmd[1]) if cmd[1:] and cmd[1].isdigit() and int(cmd[1]) in range(3, 35)
                         else 'aо' * random.randrange(3, 35)).title()

    elif cmd[0] == 'bd':
        send_back('Подождите, это займёт некоторое время…', message)
        from VKBotSearchBD import search_bd
        s = 0
        if len(cmd) > 1:
            for i in cmd[1:]:
                if i.split('/')[-1].strip('id').isdigit():
                    s = int(i.strip('https://').strip('vk.com/').strip('id'))
        bd = search_bd(s if s else message['uid'])
        age = str(bd['age'])
        age = "%s %s" % (age, 'год' if int(age[-1]) == '1' else ('годa' if int(age[-1]) in range(2, 5) else 'лет'))\
            if age else "возраст не распозднан"
        if bd['month'] == 0 and bd['day'] == 0 and bd['year'] == 0:
            return '@!' + age
        return "@!Дата рождения: %.2d.%.2d.%.4d (%s)" % (bd['day'], bd['month'], bd['year'], age)

    elif cmd[0] in ['?', 'help', 'h']:
        return '@!' + command_help(cmd[1] if len(cmd) == 2 else None)

    elif cmd[0] in ['wop', 'цщз']:
        return cmd_wop(message)

    else:
        send_back('Команды "%s" не существует\n%s' % (cmd[0], helpcmd), message)
    return 'complete'
