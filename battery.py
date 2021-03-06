def battery(mode=''):
    from command_res import command_res
    mode = mode.strip().strip('-') if type(mode) is str else None
    raw = str(command_res("acpi%s" % (' -' + mode if mode else '')), encoding='utf-8').strip().split('\n')
    if not raw[0]:
        raise ImportError('Please, install "acpi" package:\nsudo apt install acpi')

    res = {}
    for i in raw:
        name, val = i.split(': ')
        name = name.split()
        name[1] = int(name[1])
        val = val.split(', ')
        if name[0] in res:
            if name[1] in res[name[0]]:
                res[name[0]][name[1]] += val
            else:
                res[name[0]][name[1]] = val
        else:
            res[name[0]] = {name[1]: val}

    return res


if __name__ == '__main__':
    from pprint import pprint
    pprint(battery(input('Введите режим: ')))
