import os
from website.content.retrieve import retrievePrivateJson
from website.paths import PRIV_DIR
from ibisclient import createConnection, GroupMethods, PersonMethods, InstitutionMethods

""" File connects to UIS to get CRSids of all Johnians known for website access.
Stores all CRSids in txt file. Idea is this file is run periodically, say once a day,
so we're not making loads of unneccesary requests to UIS server.
Has to be run from behind the Uni firewall i.e. on the Uni network e.g. eduroam
or via the Cambridge VPN
"""

"""This commented out section shows how I got the group names for various types of
members of St. John's.


conn = createConnection()
pm = PersonMethods(conn)
me = pm.getGroups('crsid','jfc43') # Getting Johns Undergrad ID String
brian = pm.getGroups("crsid","ba364") # Getting Johns Postgrad ID String
hynes = pm.getGroups("crsid", "aw329") # Getting general members of Johns group

print('My groups')
for group in me:
    print(group.groupid, group.description)
    print(group.name)

print('Hynes groups')
for group in hynes:
    print(group.groupid, group.description)
    print(group.name)

print('Brian groups')
for group in brian:
    print(group.groupid, group.description)
    print(group.name)
"""

johnian_dump = os.path.join(PRIV_DIR, "config/johnians.txt")


def get_johnian_crsids():
    """Make request to UIS to retrieve all johnians
    Dump in johnians.dump file
    johnian.identifier.value is crsid
    """

    conn = createConnection()
    im = InstitutionMethods(conn)

    ug_johnians = [johnian.identifier.value for johnian in im.getMembers("JOHNSUG")]
    pg_johnians = [johnian.identifier.value for johnian in im.getMembers("JOHNSPG")]
    johnian_crsids = [johnian.identifier.value for johnian in im.getMembers("JOHNS")]
    other_no = len(johnian_crsids)
    johnian_crsids += ug_johnians
    johnian_crsids += pg_johnians

    exception_crsids = list(retrievePrivateJson("config/exceptions")["users"].keys())
    johnian_crsids += exception_crsids
    johnian_crsids = set(johnian_crsids)  # Remove repeats
    total = len(johnian_crsids)

    print_str = (
        "Found {0} Unique Johnians! {1} in Undergraduates, {2} in Post-Graduates "
        "{3} in General, {4} in Exceptions".format(
            total, len(ug_johnians), len(pg_johnians), other_no, len(exception_crsids)
        )
    )

    return johnian_crsids, print_str


def update_johnian_crsids():
    """Update stored txt file of all CRSIDs.
    We store the list so that we don't have to make a request to UIS every
    time we want a list of Johnian CRSids and run this script daily to
    make sure the list is up to date"""

    johnian_crsids, print_str = get_johnian_crsids()

    with open(johnian_dump, "w") as file:  # Writing crsids to file
        for crsid in johnian_crsids:
            file.write("%s\n" % crsid)

    print(print_str)


def retrieve_johnian_crsids():
    """Returns the most up to date set of all johnian crsids.
    Any exceptions such as Johnians not found by the UIS service should
    be listed in the exceptions JSON."""
    try:
        with open(johnian_dump, "r") as file:
            johnian_crsids = file.readlines()
            johnian_crsids = [crsid.split("\n")[0] for crsid in johnian_crsids]
            return set(johnian_crsids)
    except FileNotFoundError as e:
        print(e)
        update_johnian_crsids()
        return retrieve_johnian_crsids()
