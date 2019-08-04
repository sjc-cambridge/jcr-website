import os
import json

script_dir = os.path.dirname(__file__)

def retrieveJson(filepath):
    """retrieves a parsed json object from the filepath supplie
    e.g. filepath='studentlife/glossary'"""
    path = os.path.join(script_dir, filepath + ".json")
    json_file = open(path, "r")
    json_object = json.load(json_file)
    return json_object
