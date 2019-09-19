"""Checks committee class working as expected"""
from website.helper.committee import Committee
from mock import patch
import pytest

roles = {
    "president",
    "vicepresident",
    "academic",
    "access",
    "computing",
    "ents",
    "ethical",
    "equalops",
    "facilities",
    "secretary",
    "services",
    "treasurer",
    "welfare",
    "bme",
    "internationals",
    "lgbtq",
    "disabilities",
    "women"
}


def test_committee_instantiation():
    """Tests to make sure all roles loaded correctly"""
    JCR = Committee()
    for role in roles:
        assert role in JCR


#TODO: make sure mocked function is called
@patch('website.helper.committee.email_someone')
def test_email_member(email_someone_patch):
    """Test to make sure can email all committee"""
    JCR = Committee()
    for role in roles:
        try:
            JCR.email_member("subject", "message", role)
        except Exception as e:
            print("Does not work for {}".format(role))
            raise e


@patch('website.helper.committee.email_someone')
def test_email_bogus_member(email_someone_patch):
    """Raises ValueError when trying to email non committee"""
    JCR = Committee()
    with pytest.raises(ValueError):
        JCR.email_member("subject", "message", "banter")


@patch('website.helper.committee.email_people')
def test_email_committee(email_people_patch):
    JCR = Committee()
    JCR.email_committee("subject", "message")
