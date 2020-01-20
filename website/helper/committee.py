from website.content.committee import get_committee_json
from website.helper.email import email_people, email_someone


class Committee(dict):
    """Committee object is a sub-class of dictionary (for neat indexing)
        also has email methods useful for contact us and committee pages."""

    """ TODO:
    - edit .forward function.
    - Send PDF minutes
    """

    def __init__(self):
        dict.__init__(self)
        self.committee_crsids = []
        committee_json = get_committee_json()

        for key, item in committee_json.items():
            self[key] = item
            for key2, item2 in item.items():
                if key2 == 'crsid':
                    if item2 != "None": self.committee_crsids.append(item2)
                else:  # Sub-dict, e.g. welfare officers
                    if isinstance(item2, dict):
                        self.committee_crsids.append(item2['crsid'])

        self.committee_crsids = set(self.committee_crsids)

    def email_member(self, subject, input_message, committee_role, app_pwd):
        """Email committee member"""
        if committee_role in self.keys():
            email_address = committee_role + '@sjcjcr.com'
            email_someone(subject, input_message, email_address, app_pwd)
            return "Emailed {}".format(email_address)
        else:
            raise ValueError("That role is not in the committee")

    def email_committee(self, subject, input_message, app_pwd):
        """Email entire committee"""
        committee_emails = [role + '@sjcjcr.com' for role in self.keys()]
        email_people(subject, input_message, committee_emails, app_pwd)
        return "Emailed JCR Committee"
