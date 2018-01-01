import json
__raw_token = json.load(open('VKBotToken.json'))
token, me_id, email = __raw_token['token'], __raw_token['me'], __raw_token['email']
