# from rct229.rules.rule_section1 import section1_rule1


# content of test_assert1.py
def f():
    return 4


def test_function():
    assert f() == 4


"""
def test_rule1_section1_fails_if_wwr_high():
    # Expected outcome
    # Test will fail with Proposed WWR 
    user = {'wwr': 0.5}
    baseline = {'wwr': 0.5}
    proposed = {'wwr': 0.5}

    outcomes = section1_rule1(user, baseline, proposed)

    assert outcomes['rule_passed']  == False
"""
