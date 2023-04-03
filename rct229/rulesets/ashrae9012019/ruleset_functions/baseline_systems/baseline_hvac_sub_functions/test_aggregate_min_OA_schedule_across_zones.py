from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.aggregate_min_OA_schedule_across_zones import (
    aggregate_min_OA_schedule_across_zones,
)


OA_schedule = [[0.2] * 8760, [0.5] * 8760, [0.05] * 8760]


def test__aggregate_min_OA_schedule_across_zones__pass():
    assert aggregate_min_OA_schedule_across_zones(OA_schedule) == [0.75] * 8760
