"""Checks auth helper functions are correct"""
from website.helper.auth import johnian_access, committee_access

# TODO: Figure out how to test auth decorators
def test_johnian_access():
    pass


def test_committee_access():
    pass


def test_postgrads():
    assert "aos27" in johnian_crsids  # Sabir
    assert "dtz21" in johnian_crsids  # Darius, added via exceptions JSON!


def test_fellows():
    assert "tph1" in johnian_crsids # Hynes
    assert "hew1001" in johnian_crsids # Watson
