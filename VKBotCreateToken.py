try:
    import vk_api, json
    login = input('Введите логин: ')
    pwd = input('Введите пароль: ')
    print('\rПожалуйста, подождите…', end='', flush=True)
    VkAPI = vk_api.VkApi(login, pwd)
    VkAPI.auth()
    res = {'login': login, "token": VkAPI.token['access_token'],
           'pwd': pwd, 'me': VkAPI.token['user_id'], 'email': VkAPI.token['email']}

    with open('VKBotLoginData.json', 'w') as file:
        file.write(json.dumps(res, indent=4))

    print("\rВаш E-Mail: %s;\nСсылка на Ваш аккаунт: https://vk.com/id%s" % (res['email'], res['me']), flush=True)

except Exception as err:
    print("\rОШИБКА! (%s): %s\nПожалуйста, повторите попытку." % (type(err).__name__, err), flush=True)
