"""Tests to make sure emailing is set up correctly"""
from website.helper.email import email_someone, email_people
from mock import patch


# TODO: check emails are actually sent rather than just patching smtplib


@patch("website.helper.email.smtplib")
def test_email_someone(smtplib_patch):
    email_someone("subject", "message", "test@gmail.com")


@patch("website.helper.email.smtplib")
def test_email_people(smtplib_patch):
    email_people("subject", "message", ["test@gmail.com"])
