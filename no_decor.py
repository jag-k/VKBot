def no_decor(s):
    text = ''
    normal = True
    for i in s:
        if i == '\x1b':
            normal = False
        if i == 'm' and not normal:
            normal = True
            continue
        if normal:
            text += i
    return text