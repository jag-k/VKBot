def edit(**var):
    import json
    with open('params.json', 'w') as file:
        file.write(json.dumps(var, indent=4))
