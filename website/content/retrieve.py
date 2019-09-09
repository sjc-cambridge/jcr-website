import os
import json

script_dir = os.path.dirname(__file__)


def retrieveJson(filepath):
    """retrieves a parsed json object from the filepath supplied
    the .json suffix is optional
    e.g. filepath='studentlife/glossary'"""

    filepath = str(filepath).replace(".json", "") # remove json if present
    path = os.path.join(script_dir, filepath + ".json")
    json_file = open(path, "r")
    json_object = json.load(json_file)
    return json_object


def retrieveBinary(filepath):
    """Reads specified file and returns binary"""

    path = os.path.join(script_dir, filepath)
    with open(path, "rb") as file:
        return file.read()
