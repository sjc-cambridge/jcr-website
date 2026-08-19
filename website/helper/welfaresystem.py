import datetime


def userhash(crsid):
    """Convert the user + current week to a unique, unidentifiable 6 digit code
    that changes weekly. Unidentifiable since the hash seed is random by default.
    (Sidenote: Otherwise you could test all CRSids for a match!)

    Could be used to limit users to one request a day/week in future if we used
    a fully Pythonic welfare system (HTML form) but that's probably overkill."""

    this_week = str(datetime.date.today().isocalendar()[1])
    hashstring = crsid + this_week
    user_code = str(abs(hash(hashstring)))[:6]
    return user_code
