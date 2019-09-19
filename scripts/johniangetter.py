from ibisclient import createTestConnection, GroupMethods, PersonMethods
import pickle
import os
from pathlib import Path

''' File connects to UIS to get CRSids of all Johnians known for website access.
Stores all CRSids in pickled list. Idea is this file is run periodically, say once a day,
so we're not making loads of unneccesary requests to UIS server.
Has to be run from behind the Uni firewall i.e. on the Uni network e.g. eduroam
or via the Cambridge VPN
'''

'''This commented out section shows how I got the group names for various types of
members of St. John's in case these change for any reason and need to  be re-found.
Used myself, an old friend and DoS to get IDs!'''

'''
conn = createTestConnection()
pm = PersonMethods(conn)
me = pm.getGroups('crsid','jfc43') # Getting Johns Undergrad ID String
marcus = pm.getGroups("crsid","dtz21") # Getting Johns Postgrad ID String
hynes = pm.getGroups("crsid", "aw329") # Getting general members of Johns group

print('My groups')
for group in me:
    print(group.groupid, group.description)
    print(group.name)

print('Hynes groups')
for group in hynes:
    print(group.groupid, group.description)
    print(group.name)

print('Marcus groups')
for group in marcus:
    print(group.groupid, group.description)
    print(group.name)
'''

script_dir = os.path.dirname(__file__)
parent_dir = Path(script_dir).parent
johnian_dump = os.path.join(parent_dir, "website/helper/johnians.dump")

def update_johnians_crsids():
    """Make request to UIS to retrieve all johnians
    Dump in johnians.dump file"""
    conn = createTestConnection()

    gm = GroupMethods(conn)
    johnians = gm.getMembers('johnsug-members') +\
        gm.getMembers('johnspg-members') +\
        gm.getMembers('johns-members')
    johnian_crsids = []

    for johnian in johnians:
        crsid = johnian.identifier.value
        johnian_crsids.append(crsid)

    with open(johnian_dump, "wb") as file:   # Pickling
        """We store the list so that we don't have to make a request to UIS every
            time we want a list of Johnian CRSids and run this script daily to
            make sure the list is up to date."""
        pickle.dump(johnian_crsids, file)

if __name__ == "__main__":
    # Being run as script => update johns list
    update_johnians_crsids()
