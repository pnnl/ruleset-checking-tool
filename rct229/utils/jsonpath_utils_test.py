import pytest
from jsonpath_utils import find_all

# Testing find_all()
test_obj1 = {"transformers": [{"name": "tr1"}, {"name": "tr2"}, {"name": "tr3"}]}


def test__find_all__names():
    assert find_all("transformers[*].name", test_obj1) == ["tr1", "tr2", "tr3"]


def test__find_all__empty():
    assert find_all("transformers[*].id", test_obj1) == []
