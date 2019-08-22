import datetime

def userhash(auth_decorator):
    '''Convert the user + current date to a unique, unidentifiable 6 digit code.
    Could be used to limit users to one request a day. Currently unused.'''
    crsid = auth_decorator.principal
    today = str(datetime.date.today())
    if crsid:
        hashstring1 = crsid+today
        hashstring2 = 'jfc42'+today
        my_code = str(abs(hash(hashstring1)))[:6]
        similar_user_code = str(abs(hash(hashstring2)))[:6]
        print("My code:", my_code)
        print("Other user code:", similar_user_code) # Example showing hashing
    else:
        print(None)
