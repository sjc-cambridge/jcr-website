"""Checks time helper functions are correct"""

from website.helper.timehelper import (
    get_current_academic_year,
    get_year_range,
    get_academic_year,
)
import datetime


def test_get_academic_year():
    """Tests function to ensure wrapping occurs at September (month 9)"""
    assert (get_academic_year(3, 2020) == "2019-2020") is True
    assert (get_academic_year(8, 2020) == "2019-2020") is True
    assert (get_academic_year(9, 2020) == "2020-2021") is True
    assert (get_academic_year(12, 2020) == "2020-2021") is True


def test_get_current_academic_year():
    """Tests to make sure get_current_academic_year works given get_academic_year works"""
    today = datetime.date.today()
    assert (
        get_current_academic_year() == get_academic_year(today.month, today.year)
    ) is True


def test_get_year_range():
    """Makes sure gets previous and current academic years"""
    today = datetime.date.today()
    current_academic_year = get_academic_year(today.month, today.year)
    previous_academic_year = get_academic_year(today.month, today.year - 1)
    past_two_years = get_year_range()
    assert (len(past_two_years) == 2) is True
    assert current_academic_year in past_two_years
    assert previous_academic_year in past_two_years
