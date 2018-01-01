from VKBotLib import *
import requests.exceptions

# <!==Code body==!>

launch = 0 if len(sys.argv) == 1 else int(sys.argv[1])

botVersion = '2.1.0 Lib+'
version = '🐩 Версия бота: ' + botVersion + '\n📘 Версия библиотеки: ' + libVersion

try:
    print('bot start; Repeat №%d' % launch)
    sendMe('Bot On %s💬\n(%s)' % ('(repeat: %d) ' % launch if launch else '', time.asctime()))
    # print(version)
except BaseException as err:
    input(str(err)+"\n\nPress Enter to exit")
    exit()
time_date = time.asctime()
while True:
    try:
        time.sleep(1.2)
        time_date = time.asctime()
        # print('Date: '+' '.join(TimeDate.split()[1:4]))
        last_msg_id = api.storage.get(**{'key': 'last_msg_id', 'global': 1})
        message = api.messages.get(count=1, last_message_id=last_msg_id)
        if len(message) == 1:
            continue
        else:
            message = message[1]
        api.storage.set(**{'key': 'last_msg_id', 'value': message['mid'], 'global': 1})

        print(message)

        if message['uid'] in tryId or message['out']:
            if not message['body'].startswith('[id173996641|🐩 JksBot]: '):
                print(message)
                print(message['body'])
                api.storage.set(**{'key': 'last_msg_id', 'value': message['mid'], 'global': 1})
                cmd = message['body']
                if cmd:
                    if cmd[0] == '/':
                        cmd = cmd[1:].split()
                        print('Command:', cmd)
                        cmdRes = command(cmd, message)
                        print('Result: "'+str(cmdRes)+'"')
                        if type(cmdRes) == str:
                            if cmdRes[:2] == "@!":
                                sendBack(cmdRes[2:], message)
                            elif cmdRes == 'break':
                                break
                            elif cmdRes == 'version':
                                sendBack([id] + version[1:], message, noBot=True)
                            elif cmdRes == 'restart':
                                from os import system
                                system('python3 VKBot.py %d' % launch + 1)
                                sys.exit()

    except VkException as err:
        prt = 'Ошибка 🔥: type: %s\n"%s"\n\n%s' % (type(err), err, errorTime(time_date))
        print('error "'+str(err)+'"')
        print(prt)
        sendMe(prt)
    except requests.exceptions.ReadTimeout:
        err = 'У меня опять проблемка с соединением('
        print(err)
        sendMe(err)
try:
    microkey = 'Bot Off ⛔\n('+time.asctime()+')'
    sendBack(microkey, message)
    sendMe(microkey+' (sendMe)')
except BaseException as err:
    input(str(err)+"\n\nPress Enter to exit")
    exit()

# {'mid': 197944, 'date': 1490992111, 'out': 1, 'uid': 293120870, 'read_state': 0,
#  'title': ' ... ', 'body': '',
#  'fwd_messages': [{'uid': 173996641, 'date': 1490991843,
#                    'body':
#                        '''[id173996641|🐩 JksBot]: Ошибка 🔥: <br><br>name 'kok' is not defined
#                        Время и дата ошибки: Fri Mar 31 23:24:04 2017''', 'emoji': 1}]}

