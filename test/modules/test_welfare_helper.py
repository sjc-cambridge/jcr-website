"""Checks welfare system helper functions are correct"""

from website.helper.welfaresystem import userhash


def test_user_hash():
    """Tests function to ensure wrapping occurs at September (month 9)"""
    hash_one = userhash("lpt30")
    hash_two = userhash("jfc43")
    assert (hash_one == hash_two) is False
