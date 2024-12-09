import pytest
from rct229.rulesets.ashrae9012019.ruleset_functions.aggregate_min_OA_schedule_across_zones import (
    aggregate_min_OA_schedule_across_zones,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import RCTFailureException

OA_schedule = [
    [0.2 * ureg("meter")] * 8760,
    [0.5 * ureg("meter")] * 8760,
    [0.05 * ureg("meter")] * 8760,
]

OA_schedule_empty_schedule = [[], [0.5] * 8760]

OA_schedule_wrong_length = [[0.2] * 8760, [0.5] * 8760, [0.05] * 8000]


def test__aggregate_min_OA_schedule_across_zones__pass():
    assert (
        aggregate_min_OA_schedule_across_zones(OA_schedule)
        == [0.75 * ureg("meter")] * 8760
    )


def test__aggregate_min_OA_schedule_across_zones__empty_schedule():
    with pytest.raises(
        RCTFailureException,
        match="The provided list of schedules is an empty list.",
    ):
        aggregate_min_OA_schedule_across_zones(OA_schedule_empty_schedule)


def test__aggregate_min_OA_schedule_across_zones__wrong_length():
    with pytest.raises(
        RCTFailureException,
        match="Not all schedules length is equal to 8760 or 8784 or equal each other.",
    ):
        aggregate_min_OA_schedule_across_zones(OA_schedule_wrong_length)
