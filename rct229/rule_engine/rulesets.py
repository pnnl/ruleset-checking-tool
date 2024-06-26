# Ruleset enumerator
class RuleSet:
    ASHRAE9012019_RULESET = "ashrae9012019"


class RuleSetTest:
    ASHRAE9012019_TEST_LIST = [
        "section1",
        "section4",
        "section5",
        "section6",
        "section10",
        "section16",
        "section18",
        "section19",
        "section21",
        "section22",
        "section23",
    ]


class LeapYear:
    LEAP_YEAR_HOURS = 8784
    REGULAR_YEAR_HOURS = 8760


class SectionTitle:
    ASHRAE9012019_SECTION_DICT = {
        "1": "Performance Calculations",
        "4": "Schedules Setpoints",
        "5": "Envelope",
        "6": "Lighting",
        "10": "HVAC General",
        "12": "Receptacles",
        "15": "Transformers",
        "16": "Elevators",
        "18": "HVAC-Baseline",
        "19": "HVAC-General",
        "21": "HVAC-HotWaterSide",
        "22": "HVAC-ChilledWaterSide",
        "23": "HVAC-AirSide",
    }  # TODO: need to check the section titles
    ASHRAE9012019_SECTION_LIST = [
        "All",
        "Performance Calculations",
        "Schedules Setpoints",
        "Envelope",
        "Lighting",
        "HVAC General",
        "Receptacles",
        "Transformers",
        "Elevators",
        "HVAC-Baseline",
        "HVAC-General",
        "HVAC-HotWaterSide",
        "HVAC-ChilledWaterSide",
        "HVAC-AirSide",
    ]  # TODO: need to expand as more sections are developed
