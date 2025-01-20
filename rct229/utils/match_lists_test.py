import pytest
from rct229.utils.match_lists import match_lists


# Testing match_lists()
def test__match_lists__with_matching_lists():
    assert match_lists(
        [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        [{"name": "B"}, {"name": "A"}, {"name": "C"}],
        "/name",
    ) == [{"name": "A"}, {"name": "B"}, {"name": "C"}]


def test__match_lists__with_nonmatching_lists_1():
    assert match_lists(
        [{"name": "A"}, {"name": "B", "num": 8}, {"name": "C"}],
        [{"name": "H"}, {"name": "A"}],
        "/name",
    ) == [{"name": "A"}, None, None]


def test__match_lists__with_nonmatching_lists_2():
    assert match_lists(
        [{"name": "H"}, {"name": "A"}],
        [{"name": "A"}, {"name": "B", "num": 8}, {"name": "C"}],
        "/name",
    ) == [None, {"name": "A"}]
