def create_json(name, param, only_name=True):
    import json
    open(('json_files/%s.json' if only_name else '%s') % name, 'w').close()
    with open(('json_files/%s.json' if only_name else '%s') % name, 'w') as file:
        file.write(json.dumps(param, indent=2))
