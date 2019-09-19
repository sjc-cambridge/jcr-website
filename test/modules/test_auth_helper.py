"""Checks auth helper functions are correct"""
from website.helper.auth import johnian_crsids


def test_undergrads():
    assert "am2686" in johnian_crsids # Mercer
    assert "lpt30" in johnian_crsids  # Tray
    assert "ojrb2" in johnian_crsids  # Barnard
    assert "jfc43" in johnian_crsids  # Carter


def test_postgrads():
    assert "aos27" in johnian_crsids  # Sabir


def test_fellows():
    assert "aw329" in johnian_crsids  # Wheeler
    assert "tph1" in johnian_crsids # Hynes
    assert "hew1001" in johnian_crsids # Watson