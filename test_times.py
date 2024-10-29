from times import time_range,compute_overlap_time
from pytest import raises

def test_given_input():

        large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
        short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
        result = compute_overlap_time(large, short)
        expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
        assert result == expected

def test_no_overlap():
        time1 = time_range("2010-01-12 10:00:00","2010-01-12 12:00:00")
        time2 = time_range("2010-01-12 13:00:00","2010-01-12 15:45:00",2,60)
        result = compute_overlap_time(time1,time2)
        expected = []
        assert result == expected

def test_several_intervals():
        three_hours_with_two_fifteen_minute_breaks = time_range("2010-01-12 10:00:00", "2010-01-12 13:00:00", 3, 900)
        two_ranges_splitting_the_first_break = time_range("2010-01-12 10:40:00", "2010-01-12 11:20:00", 2, 120)
        expected = [("2010-01-12 10:40:00","2010-01-12 10:50:00"), ("2010-01-12 11:05:00", "2010-01-12 11:20:00")]
        assert compute_overlap_time(three_hours_with_two_fifteen_minute_breaks, two_ranges_splitting_the_first_break) == expected

def test_touching_edges():
    before = time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")
    after = time_range("2010-01-12 11:00:00", "2010-01-12 12:00:00")
    expected = []
    assert compute_overlap_time(before, after) == expected

def test_backwards_time():
    with raises(ValueError):
        assert time_range("2010-01-12 10:45:00","2010-01-12 10:30:00",2, 60)