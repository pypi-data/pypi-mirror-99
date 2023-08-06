"""Tests for past-time."""
import datetime
import unittest

from freezegun import freeze_time

from past_time import Days

DATE = "2019-11-12"


@freeze_time(DATE)
class TestPastTime(unittest.TestCase):
    """Test past-time."""

    def test_date(self):
        """Test if the mocking works."""
        assert datetime.datetime.now() == datetime.datetime(2019, 11, 12)

    def test_standard_calculation(self):
        """Test the calculations."""
        day = Days()

        assert day.days_till_end_year == 49
        assert day.total_days == 364
        assert day.passed_days == 315
        assert round(day.percent_days) == 87
