# Functions for evaluating rules

def _assert_rule(val):
    return val

def _assert_equal_rule(user_value, expected_value):
    if user_value == expected_value:
        return True
    else:
        return False

def _compare_rule(val):
    return val

def _select_equal_or_greater(input_value, reference_value):
    if input_value >= reference_value:
        return input_value
    else:
        return reference_value

def _select_equal_or_lesser(input_value, reference_value):
    if input_value <= reference_value:
        return input_value
    else:
        return reference_value