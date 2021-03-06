from VKBotAPI import LOGIN_DATA, api
import requests
token = LOGIN_DATA['token']
api_url = 'https://api.vk.com/method/docs.get%sUploadServer'


def doc_save(*files_data, doc_type='doc'):
    """
    :param files_data: полученые строки после загрузки файлов
    :param doc_type: тип фалов ('photo', 'video', 'audio', 'doc', 'wall', 'market')
    :return: строка для attachment
    """
    if doc_type == 'audio_message':
        doc_type = 'doc'
    res = [api.docs.save(file=i)[0] for i in files_data]
    return ','.join("%s%s_%s" % (doc_type, i['owner_id'], i['id']) for i in res)


def upload_doc(file, type='doc', peer_id=LOGIN_DATA['me'], server='Messages'):
    """
    :param file: Файл для загрузки (open(*file_name*, 'rb') or bytes)
    :param type: Тип файла ('photo', 'video', 'audio', 'doc', 'wall', 'market')
    :param peer_id: куда
    :param server: Куда отправлять ('Messages' - для сообщений, 'Wall' - на стену или в лс, '' - для загрузки в файлы)
    :return: doc_save()
    """
    url = api_url % server.title()
    params = {
        'type': type,
        'peer_id': peer_id,
        "access_token": token,
        'version': '5.73'
    }
    res = requests.get(url, params).json()

    upload_url = res['response']['upload_url']

    data = {'file': file}
    res = requests.post(upload_url, files=data).json()['file']

    return doc_save(res, doc_type=type)


if __name__ == '__main__':
    file = open("audio/Test.ogg", 'rb')
    pid = 65847488
    pid = LOGIN_DATA['me']
    from VKBotLib import set_activity
    set_activity(pid)
    attachment = upload_doc(file, 'audio_message', pid)
    api.messages.send(message="Отправил с бота))", attachment=attachment, user_id=pid)
