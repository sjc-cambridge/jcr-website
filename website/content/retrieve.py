import os
import json

from website.paths import PRIV_DIR

script_dir = os.path.dirname(__file__)


def _load_json(root, filepath):
    filepath = str(filepath).replace(".json", "")  # remove json if present
    path = os.path.join(root, filepath + ".json")
    with open(path, "r") as json_file:
        json_object = json.load(json_file)
    return json_object


def retrieveJson(filepath):
    """
    Retrieves a parsed json object from the filepath supplied
    the .json suffix is optional
    e.g. filepath='studentlife/glossary'
    """
    return _load_json(script_dir, filepath)


def retrievePrivateJson(filepath):
    """As retrieveJson, but rooted in the private data directory."""
    return _load_json(PRIV_DIR, filepath)


def retrieveBinary(filepath):
    """Reads specified file and returns binary"""
    path = os.path.join(script_dir, filepath)
    with open(path, "rb") as file:
        return file.read()
