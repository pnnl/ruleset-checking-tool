import pytest
from jsonpath_utils import (
    find_all,
    find_all_with_field_value,
    find_one_with_field_value,
)

# Testing find_all()
test_obj1 = {"transformers": [{"name": "tr1"}, {"name": "tr2"}, {"name": "tr3"}]}


def test__find_all__names():
    assert find_all("transformers[*].name", test_obj1) == ["tr1", "tr2", "tr3"]


def test__find_all__empty():
    assert find_all("$.transformers[*].id", test_obj1) == []


def test__find_all_with_field_value():
    assert find_all_with_field_value("transformers[*]", "name", "tr2", test_obj1) == [
        {"name": "tr2"}
    ]
    assert find_one_with_field_value("transformers[*]", "name", "tr2", test_obj1) == {
        "name": "tr2"
    }
