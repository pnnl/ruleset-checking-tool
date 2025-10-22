from rct229.ruletest_engine.ruletest_jsons.ashrae9012019 import (
    ELEVATOR_DIR,
    ENVELOPE_DIR,
    HVAC_AIRSIDE_DIR,
    HVAC_BASELINE_DIR,
    HVAC_CHILLED_WATER_DIR,
    HVAC_GENERAL_DIR,
    HVAC_HOT_WATER_DIR,
    LIGHTING_DIR,
    PERFORMANCE_CALC_DIR,
    RECEPTACLE_DIR,
    SCHEDULE_DIR,
    SERVICE_HOT_WATER_DIR,
)


# Ruleset enumerator
class RuleSet:
    ASHRAE9012019_RULESET = "ashrae9012019"
    ASHRAE9012022_RULESET = "ashrae9012022"


class RuleSetTest:
    ASHRAE9012019_TEST_LIST = [
        PERFORMANCE_CALC_DIR,     # Section 1
        ELEVATOR_DIR,             # Section 16
        ENVELOPE_DIR,             # Section 5
        HVAC_AIRSIDE_DIR,         # Section 23
        HVAC_CHILLED_WATER_DIR,   # Section 22
        HVAC_GENERAL_DIR,         # Section 10 & 19
        HVAC_HOT_WATER_DIR,       # Section 21
        HVAC_BASELINE_DIR,        # Section 18
        LIGHTING_DIR,             # Section 6
        RECEPTACLE_DIR,           # Section 12
        SCHEDULE_DIR,             # Section 4
        SERVICE_HOT_WATER_DIR,    # Section 11
    ]
    ASHRAE9012022_TEST_LIST = [
        ENVELOPE_DIR,             # Section 5
    ]


class LeapYear:
    LEAP_YEAR_HOURS = 8784
    REGULAR_YEAR_HOURS = 8760
