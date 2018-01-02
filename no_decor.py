def no_decor(s):
    text = ''
    normal = True
    for i in s:
        if i == '\x1b':
            normal = False
        if i == 'm':
            normal = True
        if normal:
            text += i
    return text