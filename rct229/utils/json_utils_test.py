import pytest
from rct229.utils.json_utils import slash_prefix_guarantee


# Testing slash_prefix_guarantee
def test__slash_prefix_guarantee__with_slash():
    assert slash_prefix_guarantee("/pointer") == "/pointer"


def test__slash_prefix_guarantee__without_slash():
    assert slash_prefix_guarantee("pointer") == "/pointer"
