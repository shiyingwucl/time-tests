from times import time_range,compute_overlap_time
import pytest
import yaml

input_expected = [(time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
  time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
  [("2010-01-12 10:30:00","2010-01-12 10:37:00"), ("2010-01-12 10:38:00", "2010-01-12 10:45:00")]),

  (time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
  time_range("2010-01-12 12:30:00", "2010-01-12 12:45:00", 2, 60),
  []),

  (time_range("2010-01-12 10:00:00", "2010-01-12 13:00:00", 3, 900),
  time_range("2010-01-12 10:40:00", "2010-01-12 11:20:00", 2, 120),
  [("2010-01-12 10:40:00","2010-01-12 10:50:00"), ("2010-01-12 11:05:00", "2010-01-12 11:20:00")]),

  (time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
  time_range("2010-01-12 11:00:00", "2010-01-12 12:45:00"),
  [])]

@pytest.mark.parametrize("time1, time2, expected_overlap",input_expected)
def test_overlap(time1,time2,expected_overlap):
        assert compute_overlap_time(time1,time2) == expected_overlap

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
    with pytest.raises(ValueError):
        assert time_range("2010-01-12 10:45:00","2010-01-12 10:30:00",2, 60)

def load_fixture_data():
        with open("fixture.yaml") as file:
                fixture = yaml.safe_load(file) # loading yaml returns a list
                return fixture
      

test_data = []

fixture = load_fixture_data()

for case in fixture:
        start_1 = case.keys()[0]["time_range_1"]["start"] # needs to convert to list since .keys() returns a view object
        end_1 = case.keys()[0]["time_range_1"]["end"]
        intervals_1= case.keys()[0]["time_range_1"]["intervals"]
        time_between_interval_1 = (case.keys())[0]["time_range_1"]["time_between_intervals"]
        range1 = time_range([start_1,end_1,intervals_1,time_between_interval_1])

        start_2 = (case.keys()[0]["time_range_2"]["start"])
        end_2 = (case.keys()[0]["time_range_2"]["end"])
        intervals_2= (case.keys())[0]["time_range_2"]["intervals"]
        time_between_interval_2 = (case.keys())[0]["time_range_2"]["time_between_intervals"]
        range2 = time_range([start_2,end_2,intervals_2,time_between_interval_2])

        expected = case.keys()[0]["expected"]

        test_data.append([range1,range2,expected])

@pytest.mark.parametrize("range1, range2, expected", test_data)
def test_compute_overlap_time(range1, range2, expected):
       assert compute_overlap_time(range1,range2) == expected