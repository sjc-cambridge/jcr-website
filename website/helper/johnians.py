import pickle
import os
from website.content.retrieve import retrieveJson

script_dir = os.path.dirname(__file__)
johnian_dump = os.path.join(script_dir, "johnians.dump")

def retrieve_johnian_crsids():
    """Returns the most up to date set of all johnian crsids.
        Any exceptions such as Johnians not found by the UIS service should
        be listed in the exceptions JSON."""
    exception_crsids = list(retrieveJson("config/exceptions")["users"].keys())
    with open(johnian_dump, "rb") as file:
        johnian_crsids = pickle.load(file)
        return set(johnian_crsids+exception_crsids)
