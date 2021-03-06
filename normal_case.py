def normal_case(s: str):
    res = ['']
    for i in s:
        if i == i.upper():
            res.append(i.lower())
        else:
            res[-1] += i
    return '_'.join(filter(lambda x: x, res))
