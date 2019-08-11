import ucam_webauth
import ucam_webauth.raven
import ucam_webauth.raven.flask_glue
import os
import pickle

script_dir = os.path.dirname(__file__)

with open(os.path.join(script_dir, "johnians.txt"), "rb") as file:
    johnian_crsids = set(pickle.load(file))

#johnian_crsids.remove('jfc43') #Testing login works

auth_decorator = ucam_webauth.raven.flask_glue.AuthDecorator(max_life = 15,
                                            require_principal = johnian_crsids)


class Committee(dict):
    ''' TODO: Dictionary keys are role emails @sjcjcr.com,
     could have email to all methods etc.
     Could also edit .forward file from this.
    '''
    def __init__(self, committee_text_file, *args):
        dict.__init__(self, args)
        self.path = os.path.join(script_dir, committee_text_file)
        self.text_file = open(self.path, "r")
        self.lines = self.text_file.readlines()
        for line in self.lines:
            line = line.split('\n')[0]
            role, names, crsids = line.split(' ')
            names = names.split('/') # Split any co presidents!!
            crsids = crsids.split('/')
            names = ' & '.join(names)
            crsids = ' & '.join(crsids)
            self[role] = dict()
            self[role]['name']=names
            self[role]['crsid']=crsids
        self.text_file.close()


JCR = Committee("committee.txt")
'''
print(JCR)
print(JCR['PRESIDENT']['name'])
print(JCR['COMPUTING']['name'])'''
