import vk_api, json, vk
#тестовая реализация VKBotAPI на vk_api
# while True:
#     try:
#         login = json.load(open('VKBotLoginData.json'))
#         session = vk_api.VkApi(login=login['login'], password=login['pwd'], token=login['token'])
#         break
#     except Exception:
#         import VKBotCreateToken
#
# try:
#     session.auth()
# except Exception as e:
#     print("Error",e)
# api = session.get_api()  # Нужно для работы API VK
LOGIN_DATA = json.load(open('VKBotLoginData.json'))
session = vk.Session(access_token=LOGIN_DATA['token'])
API_VERSION = 5.72
api = vk.API(session, version=API_VERSION)
