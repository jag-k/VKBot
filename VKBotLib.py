__author__ = "Jag_k"
import time

# from VKBotAudioMessage import *
from VKBotAPI import *
from VKBotNote import *
from color import color
import sys
from vk.exceptions import VkException
# from speaker import Speak, KEY

print('lib import done')

libVersion = '0.1.7'

note = [Note("Заметки"), Note("Test", [['lol', False]])]
noteCount = 1
admins = [173996641, 316261212]
tryId = [173996641, 316261212, 366459937, 366930057, 22366930057, 252168745, 443841821, 192238236]
edit_table = [173996641, 12306618]

helpcmd = 'Укажите, что вы хотите сделать: для этого можете обратиться к справке, выполнив запрос "/? {команда}" или сделав запрос "/?" для получения всей справки о командах.'


cmds = { # ['Описание','Аргументы (Если нет, то None)','Примечание (если это команда уровня Адимнистрации, то 'admin') (Если None, то не имеет примечания)']
    '/?': ['Позволяют получить список команд', '{название любой команды без символа вызова команды (/)}', 'при вводе без аргумента выводится весь список допустимых команд.', None],
    # '/say': ['Говорит фразу синтезированным голосом', '{текст для произношения}', None],
    '/show': ['Показывает какую-либо информацию (например показывает списки администраторов и список доверенных людей или Токен "Всевластья")','token, admin_list, try_id', 'admin'],
    '/stop': ['Останавливает бота', None, 'доступно только [id173996641|Сигизмунду Конону] и ещё нескольким людям'],
    # '/add': ['Позволяет добавить что-либо куда либо (напрмер даёт возможность добавить администратора к боту, добавить бота к беседе или добать/изменить значение переменной)','admin {id пользователя} и people {id пользователя}', None],
    '/version': ['Выводит номера версий библиотеки, бота и кодировщика', None, None],
    # '/sleep': ['Вводит бота в режим сна', '{секунды}, {минуты}, {часы}', 'admin'],
    '/id': ['Выводит Ваш id', None, None],
    '/note': ['Выводит заметки', 'вызов без аргументов показывает заметки, add - добавить заметку, edit - изменить существующую заметку, del - удалить заметку',None]
}
'''
#Функции

#Table

def post(message, groupId = id_group):
    return api.wall.post(**{'owner_id': groupId, 'from_group': 1, 'message':message})

def editPost(message, post_id, groupId = id_group):
    try: api.wall.edit(**{'owner_id':groupId,'post_id':post_id,'message':message})
    except BaseException: return post(message, groupId)
    return {'post_id': post_id}

def lastPost(Type = 'table', date = False, groupId = id_group): #Type == 'table' or 'hw'
    if not date:
        post = api.wall.search(**{'owner_id':groupId,'query':Type+' ','count':1,'extended':0})
        if len(post) != 1:
            return post[1]
    else:
        post = api.wall.search(**{'owner_id':groupId,'query':Type+' '+date,'count':1,'extended':0})
        if len(post) != 1:
            return post[1]
    return [0]

def table_and_hw(table, hw): pass

#end Table
'''


def sayBot(text, noBot):
    if noBot:
        return text
    return '[id173996641|🐩 JksBot]: ' + text


def sendMe(text, noBot=False):
    time.sleep(0.25)
    api.messages.send(**{'domain': 'jag_k58', 'message': sayBot(text, noBot)})


def sendBack(text, message, noBot=False, attachment='', fwd=[]):
    if message['title'] == '' and str(message['uid'])[0] == '-':
        api.messages.send(**{'peer_id': message['uid'], 'message': sayBot(text, noBot), 'attachment': attachment,
                             "forward_messages": ','.join(map(str, fwd))})
    elif message['title'] == '':
        api.messages.send(**{'user_id': message['uid'], 'message': sayBot(text, noBot), 'attachment': attachment,
                             "forward_messages": ','.join(map(str, fwd))})
    elif message['title'] != '':
        api.messages.send(**{'chat_id': message['chat_id'], 'message': sayBot(text, noBot), 'attachment': attachment,
                             "forward_messages": ','.join(map(str, fwd))})


def relevant(message): return '[id'+str(message['uid'])+'|'+api.users.get(**{'user_ids':message['uid']})[0]['first_name']+'], '


def errorTime(TimeDate): return 'Время и дата ошибки: '+TimeDate


def commandHelp(c, full=False):  # ['Описание','Аргументы (Если None, то )','Примечание (если это команда уровня Адимнистрации, то True) (Если False, то не имеет примечания)']
    if not full:
        cmd = cmds['/' + c]
        txt = '• /' + c + ': ' + cmd[0]

    else:
        cmd = cmds[c]
        txt = '• ' + c + ': ' + cmd[0]

    if cmd[1] is None:
        txt += '\n📝 Не имеет аргументов'

    else:
        txt += '\n📝 Имеет аргументы: '+cmd[1]

    if cmd[2] == 'admin':
        return txt+'\n⚠ Примечание: большинством функционала данной команды могут пользоваться только администраторы!'

    elif cmd[2] is None:
        return txt

    return txt+'\n⚠ Примечание: '+cmd[2]


def command(cmd, message):  # 0 == break, 1 == 'complete', 2 == 'version', 3 == 'result'
    import commands._edit_param as edit_param
    edit_param.edit(cmd=cmd, message=message)

    if cmd[0] == 'show' and message['uid'] in admins:  # /show
        if len(cmd) > 1:
            if cmd[1] == 'token':
                sendBack('Token: '+token, message)
            else:
                sendBack('Нет такой комманды.\n'+helpcmd, message)
        else:
            sendBack("""Вызовете эту комманду повторно, но уже с аргументом.
            Если Вы забыли или не знаете аргументов к этой команды, то напишете /? show""", message)
        
    elif cmd[0] == 'stop' and message['uid'] in admins:  # /stop
        return 'break'
    
    elif cmd[0] == 'version':
        return 'version'  # /version
    
    elif cmd[0] == 'restart':
        return 'restart'  # /restart
    
    # elif cmd[0] == 'cangelog': sendBack(history)
    
    elif cmd[0] == 'id':
        return sendBack(relevant(message)+'Ваш id: '+str(message['uid']), message)  # /id

    elif cmd[0] == 'connect':
        sendBack("The connection is successful!", message)

    elif cmd[0] == 'say':
        sendBack('', message, noBot=True, attachment=audio_message(*cmd[1:], 1))

    elif cmd[0] == 'note':
        if len(cmd) == 1:
            return '@!'+note[noteCount].name+':\n' + '\n'.join(note[noteCount].textNote())
        else:
            if cmd[1] == 'add':
                note[noteCount].addNote(' '.join(cmd[2:]))
                return '@!Заметка под номером {} была успешно добавлена в "{}"!'.format(str(len(cmd) + 1),
                                                                                        note[noteCount])
            elif cmd[1] == 'edit' and len(cmd) > 2:
                if cmd[2].isdigit():
                    if cmd[3].lower() == '*завершено*' or cmd[3].lower() == '*done*':
                        note[noteCount].editNote(int(cmd[2]), done=True,
                                                 text=(' '.join(cmd[4:]) if len(cmd) > 3 else None))
                    else:
                        note[noteCount].editNote(int(cmd[2]), text=(' '.join(cmd[4:]) if len(cmd) > 3 else None))
                    return '@!Заметка под номером {} из "{}" была успешно изменена!'.format(cmd[2], note[noteCount])
            elif cmd[1] == 'del' and len(cmd) == 3:
                if cmd[2].isdigit():
                    return '@!Заметка под номером {} из "{}" была успешно удалена!'.format(cmd[2], note[noteCount])\
                        if note[noteCount].delNote(int(cmd[2])) else \
                        note[noteCount].name + ':\n' + '\n'.join(note[noteCount].textNote())
            elif cmd[1] == 'list':
                return "@!Список заметок:\n" + "\n ".join(map(lambda x: str(note.index(x) + 1) + ') ' + str(x), note))
            elif cmd[1] == 'create' and len(cmd) > 2:
                note.append(Note(cmd[2:]))

            else:
                return '@!' + note[noteCount].name + ':\n' + '\n'.join(note[noteCount].textNote())

    elif cmd[0] == '?':  # /?
        if len(cmd) == 2:
            if '/'+cmd[1] in cmds:
                sendBack(commandHelp(cmd[1]), message)
            else:
                sendBack('Нет такой команды.\n'+helpcmd, message)
        elif len(cmd) > 2:
            sendBack('Нельзя вводить больше одного аргумента', message)
        else:
            func = '\n\n'.join(sorted([commandHelp(i, full=True) for i in cmds.keys()]))
            sendBack(func, message)
        
    elif cmd[0] == 'add':  # /add
        if cmd[1]:
            if cmd[1] == 'admin':
                if cmd[2]:
                    if cmd[2].isdigit():
                        admins.append(int(cmd[2]))
                    else:
                        sendBack('Id пользователя дожен состоять только из чисел.', message)
                else:
                    sendBack('Введите id нового администратора для бота, выполнив команду по типу "/add admin {id пользователя}".', message)
        else:
            sendBack(helpcmd, message)
    
    elif cmd[0] == 'crack' and message['uid'] in admins:
        sendBack(kok, message)

    elif cmd[0] == 'wop':
        from commands.cmd_wop import cmd_wop
        return cmd_wop()

    else:
        sendBack('Такой команды не существует\n'+helpcmd, message)
    return 'complete'


print('lib loaded')
