from VKBotAPI import *


def search_bd(user_id, shift=10):
    import time
    
    def rec_search_get(age_from, age_to, offset=0, **keys):
        try:
            res: list = api.users.search(q=' '.join([user['first_name'], user['last_name']]),
                                         offset=offset * 1000,
                                         sort=0, fields='sex', sex=user['sex'], age_from=age_from, age_to=age_to,
                                         count=1000, **keys)[1:]
        except Exception:
            time.sleep(1.001)
            res: list = api.users.search(q=' '.join([user['first_name'], user['last_name']]),
                                         offset=offset * 1000,
                                         sort=0, fields='sex', sex=user['sex'], age_from=age_from, age_to=age_to,
                                         count=1000, **keys)[1:]
        if len(res) < 1000:
            return res
        return res + rec_search_get(age_from, age_to, offset=offset+1, **keys)

    def repl(s: str):
        return ' '.join(str(int(i)) if i.isdigit() else i for i in s.split())
    
    def date_search(age):
        month = {0: 0, 1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        time.strftime("%a, %d.%m %H:%M", time.gmtime())
        year = int(time.strftime("%Y", time.gmtime()))

        for m in range(1, 13):
            time.sleep(1.001)
            rec1 = rec_search_get(age, age, birth_month=m)
            if user['uid'] in map(lambda x: x['uid'], rec1):
                time.sleep(1.001)
                for d in range(1, month[m]+1):
                    try:
                        rec2 = rec_search_get(age, age, birth_month=m, birth_day=d)
                    except Exception:
                        time.sleep(1.001)
                        rec2 = rec_search_get(age, age, birth_month=m, birth_day=d)
                    if user['uid'] in map(lambda x: x['uid'], rec2):
                        p = time.strftime("0 if %j >= " + str((d-1 + sum(map(lambda x: month[x], range(m))))) +
                                          ' else 1', time.gmtime())
                        return {'month': m, 'day': d, 'year': year - age - eval(repl(p)), 'age': age}
        return {'month': 0, 'day': 0, 'year': 0, 'age': age}
    try:
        user = api.users.get(user_ids=user_id, fields='sex')[0]
    except Exception:
        time.sleep(1.001)
        user = api.users.get(user_ids=user_id, fields='sex')[0]

    for i in range(13):
        try:
            raw = rec_search_get(i*shift, (i+1)*shift)
        except Exception:
            time.sleep(1.001)
            raw = rec_search_get(i*shift, (i+1)*shift)
        if any(user_id == us['uid'] for us in raw):
            for age in range(i*shift, (i+1)*shift):
                try:
                    r = rec_search_get(age, age)
                except Exception:
                    time.sleep(1.001)
                    r = rec_search_get(age, age)
                if user_id in map(lambda x: x['uid'], r):
                    return date_search(age)
    return 0


if __name__ == '__main__':
    for i in map(int,
                 input("Введите ID для того, что бы узнать дату рождения (можно несколько через пробел): ").split()):
        print(search_bd(i))
