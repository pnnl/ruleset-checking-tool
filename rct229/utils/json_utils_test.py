import pytest
from json_utils import to_json_pointer


# Testing slash_prefix_guarantee
def test__to_json_pointer__with_slash():
    assert to_json_pointer("/pointer") == "/pointer"


def test__to_json_pointer__without_slash():
    assert to_json_pointer("pointer") == "/pointer"


def test__to_json_pointer__without_empty_string():
    assert to_json_pointer("") == ""
