import datetime

def userhash(crsid):
    '''Convert the user + current date to a unique, unidentifiable 6 digit code.
    Could be used to limit users to one request a day in future.'''
    today = str(datetime.date.today())
    hashstring = crsid+today
    user_code = str(abs(hash(hashstring)))[:6]
    return user_code
