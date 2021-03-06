import os
import json
js_params = {}


def update_params(cwd='./json_files'):
    global js_params
    for i in os.listdir(cwd):
        if os.path.isfile(i) and i.endswith('.json'):
            exec("%s = %s" % (i[:-5], json.load(open(i))))
            js_params[i[:-5]] = eval(i[:-5])
    return js_params


if __name__ == '__main__':
     update_params(os.getcwd())
else:
    update_params()
print("js_params:", js_params)
