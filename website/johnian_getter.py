''' File connects to UIS to get CRSids of all Johns undergraduates and postgraduates.
Stores all CRSids in pickled list. Idea is this file could be run on a cronjob
(or just using datetime triggered by a website routing function),
so we're not making loads of unneccesary requests to UIS server.
Has to be run from behind the Uni firewall i.e. on the Uni network e.g. eduroam
or via the Cambridge VPN
'''

from ibisclient import *
import pickle

conn = createTestConnection()

'''This commented out section shows how I got the group names for various types of
members of St. John's in case these change for any reason and need to  be re-found.
Used myself, an old friend and DoS to get IDs!

pm = PersonMethods(conn)
me = pm.getGroups('crsid','jfc43') # Getting Johns Undergrad IDs
marcus = pm.getGroups("crsid","mjgs3") # Getting Johns Postgrad IDs
hynes = pm.getGroups("crsid", "tph1")
for group in me:
    print(group.groupid, group.description)
    print(group.name)
for group in hynes:
    print(group.groupid, group.description)
    print(group.name)
for group in marcus:
    print(group.groupid, group.description)
    print(group.name)'''

gm = GroupMethods(conn)
johnians = gm.getMembers('johnsug-members')+\
                gm.getMembers('johnspg-members')+\
                    gm.getMembers('johns-members')
johnian_crsids = []

for johnian in johnians:
    crsid = johnian.identifier.value
    johnian_crsids.append(crsid)

with open("johnians.txt", "wb") as file:   #Pickling
    pickle.dump(johnian_crsids, file)
