import json

def import_config(filename, filepath=""):    
    with open(filepath + filename) as file:
        config = json.load(file)
    return config