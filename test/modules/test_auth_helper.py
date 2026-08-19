"""Checks auth helper functions are correct"""

from website.helper.auth import johnian_access, committee_access, johnian_crsids


# TODO: Figure out how to test auth decorators
def test_johnian_access():
    pass


def test_committee_access():
    pass


def test_undergrads():
    assert "am2686" in johnian_crsids  # Mercer
    assert "lpt30" in johnian_crsids  # Tray
    assert "ojrb2" in johnian_crsids  # Barnard
    assert "jfc43" in johnian_crsids  # Carter


def test_postgrads():
    assert "aos27" in johnian_crsids  # Sabir
    assert "dtz21" in johnian_crsids  # Darius, added via exceptions JSON!


def test_fellows():
    assert "tph1" in johnian_crsids  # Hynes
    assert "hew1001" in johnian_crsids  # Watson
