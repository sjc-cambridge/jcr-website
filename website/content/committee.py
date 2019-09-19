"""Module for retrieving committee related data"""
from website.content.retrieve import retrieveJson


def get_committee_json():
    """Retrieves json object for committee.
    This is an object of format:
    {
        "rolname": {
            "role" : string,
            "name" : string,
            "crsid": string,
            "bio"  : string,
            "img"  : string
        }
    }
    The only exceptions to this are the president and welfare roles
    """
    commitee_json = retrieveJson("committee/committee")
    return commitee_json