from website.content.retrieve import retrieveJson


def get_committee_json():
    commitee_json = retrieveJson("committee/committee")
    return commitee_json