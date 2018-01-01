import json

PARAMS = json.load(open('params.json'))

for i in PARAMS:
    exec("%s = %s" % (i, PARAMS[i]))
