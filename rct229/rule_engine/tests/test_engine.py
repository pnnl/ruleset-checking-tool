# from rct229.rule_engine.engine import get_available_rules
import inspect

import rct229.rules as rules


# content of test_assert1.py
def test_get_available_rules():
    # test to check the number of available rules
    available_rules = rules.__getrules__()

    assert len(available_rules) == 6
