# /usr/bin/python3.6
from VKBotLib import *
running = True

try:
    launch = 0 if len(sys.argv) == 1 else int(sys.argv[1])

    print_log("Users: %s" % users_list)
    print_log(color("tryID:", 4, 34), users_list(1))
    print_log(color("admins:", 4, 36), users_list(2))

    print_log('bot start; Repeat №%d' % launch)
    send_me('Bot On %s💬\n(%s)' % ('(repeat: %d) ' % launch if launch else '', time.asctime()))

except Exception as err:
    error_log(err, print_stdout=False)
    input("\n\nPress Enter to exit: ")
    SystemExit()

time_date = time.asctime()
while running:
    try:
        time.sleep(1)
        time_date = time.asctime()
        dialogs = api.messages.getDialogs(offset=-20, count=20, start_message_id=last_msg_id)
        if len(dialogs) == 1:
            continue
        else:
            for message in dialogs[1:]:
                message = more_data_message(message)
                print_message_info(message)
                last_msg_id.write(message['mid'])

                if message['uid'] in users_list() or message['out']:
                    if not message['body'].startswith('[id173996641|🐩 JksBot]: '):
                        # api.storage.set(**{'key': 'last_msg_id', 'value': message['mid'], 'global': 1})
                        cmd = message['body']
                        if cmd:
                            if cmd[0] == '/':
                                cmd = cmd[1:].split()
                                print_log('\x1b[32mCommand\x1b[0m:', cmd)
                                cmd_res = command(cmd, message)
                                print_log('\x1b[35mResult\x1b[0m: "%s"' % cmd_res)

                                if type(cmd_res) is str:
                                    if cmd_res.startswith("@!"):
                                        send_back(cmd_res[2:], message)

                                    if cmd_res.startswith("@N"):
                                        send_back(cmd_res[2:], message, no_bot=True)

                                    if cmd_res.startswith("@C"):
                                        quote_edit(cmd_res[2:], message)

                                    elif cmd_res == 'break':
                                        running = False
                                        SystemExit()

                                    elif cmd_res == 'update':
                                        send_back('Обновление библиотеки началось…', message)
                                        from VKBotLib import *
                                        send_back('Обновление библиотеки успешно завершено!', message)

                                    elif cmd_res == 'restart':
                                        from os import system
                                        system('python3 VKBot.py %d' % (launch + 1))
                                        sys.exit()

    except KeyboardInterrupt:
        msg = input('Введите сообщение (%s%s): ' % (message['type'][0].upper(), message['pid'])).strip()
        if msg:
            send_back(msg, message, True)

    except VkAPIError as err:
        error_log(err)
        time.sleep(1.5)

    except Exception as err:
        error_log(err)

    except NoCallError:
        pass

try:
    microkey = 'Bot Off ⛔\n(%s)' % time.asctime()
    send_back(microkey, message)
    send_me(microkey+' (send_me)')
except BaseException as err:
    error_log(err, print_stdout=False)
    input("\n\nPress Enter to exit: ")
    exit()
