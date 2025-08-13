from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0, PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_avg_zone_height import (
    get_avg_zone_height,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.normalize_interior_lighting_schedules import (
    normalize_interior_lighting_schedules,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.masks import invert_mask
from rct229.utils.pint_utils import ZERO

BUILDING_AREA_CUTTOFF = ureg("5000 ft2")


class PRM9012019Rule08a45(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule08a45, self).__init__(
            id="6-5",
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule08a45.RulesetModelInstanceRule(),
            index_rmd=BASELINE_0,
            description="Baseline building is modeled with automatic shutoff controls in buildings >5000 sq.ft.",
            ruleset_section_title="Lighting",
            standard_section="Section G3.1-6 Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RulesetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule08a45.RulesetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule08a45.RulesetModelInstanceRule.BuildingRule(),
                index_rmd=BASELINE_0,
                list_path="buildings[*]",
                required_fields={
                    "$": ["schedules"],
                },
                data_items={
                    "schedules_b": (BASELINE_0, "schedules"),
                    "schedules_p": (PROPOSED, "schedules"),
                },
            )

        class BuildingRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    PRM9012019Rule08a45.RulesetModelInstanceRule.BuildingRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    each_rule=PRM9012019Rule08a45.RulesetModelInstanceRule.BuildingRule.ZoneRule(),
                    index_rmd=BASELINE_0,
                    list_path="$.building_segments[*].zones[*]",
                    required_fields={"$": ["building_open_schedule"]},
                    data_items={
                        "building_open_schedule_id_b": (
                            BASELINE_0,
                            "building_open_schedule",
                        ),
                    },
                )

            def is_applicable(self, context, data):
                building_b = context.BASELINE_0
                building_total_area_b = sum(
                    find_all(
                        "$.building_segments[*].zones[*].spaces[*].floor_area",
                        building_b,
                    ),
                    ZERO.AREA,
                )

                return building_total_area_b > BUILDING_AREA_CUTTOFF

            class ZoneRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super(
                        PRM9012019Rule08a45.RulesetModelInstanceRule.BuildingRule.ZoneRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                        each_rule=PRM9012019Rule08a45.RulesetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule(),
                        index_rmd=BASELINE_0,
                        list_path="spaces[*]",
                    )

                def create_data(self, context, data=None):
                    zone_b = context.BASELINE_0
                    zone_p = context.PROPOSED
                    return {
                        "avg_zone_height_b": get_avg_zone_height(zone_b),
                        "avg_zone_height_p": get_avg_zone_height(zone_p),
                    }

                class SpaceRule(RuleDefinitionBase):
                    def __init__(self):
                        super(
                            PRM9012019Rule08a45.RulesetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule,
                            self,
                        ).__init__(
                            rmds_used=produce_ruleset_model_description(
                                USER=False, BASELINE_0=True, PROPOSED=True
                            ),
                        )

                    def is_applicable(self, context, data=None):
                        # set space has no lighting space type to not applicable
                        space_b = context.BASELINE_0
                        return space_b.get("lighting_space_type") is not None

                    def get_calc_vals(self, context, data=None):
                        schedules_b = data["schedules_b"]
                        space_b = context.BASELINE_0
                        space_p = context.PROPOSED
                        building_open_schedule_id_b = data[
                            "building_open_schedule_id_b"
                        ]
                        building_open_schedule_b = find_exactly_one_with_field_value(
                            jpath="$[*]",
                            field="id",
                            value=building_open_schedule_id_b,
                            obj=schedules_b,
                        )
                        hourly_building_open_schedule_b = getattr_(
                            building_open_schedule_b,
                            "building_open_schedule_b",
                            "hourly_values",
                        )
                        schedules_b = data["schedules_b"]
                        schedules_p = data["schedules_p"]
                        space_height_b = data["avg_zone_height_b"]
                        space_height_p = data["avg_zone_height_p"]

                        normalized_interior_lighting_schedule_b = (
                            normalize_interior_lighting_schedules(
                                space_b,
                                space_height_b,
                                schedules_b,
                                adjust_for_credit=False,
                            )
                        )
                        normalized_interior_lighting_schedule_p = (
                            normalize_interior_lighting_schedules(
                                space_p,
                                space_height_p,
                                schedules_p,
                                adjust_for_credit=False,
                            )
                        )

                        schedule_comparison_result = compare_schedules(
                            normalized_interior_lighting_schedule_b,
                            normalized_interior_lighting_schedule_p,
                            mask_schedule=invert_mask(hourly_building_open_schedule_b),
                        )

                        return {
                            "schedule_comparison_result": schedule_comparison_result
                        }

                    def rule_check(self, context, calc_vals=None, data=None):
                        schedule_comparison_result = calc_vals[
                            "schedule_comparison_result"
                        ]
                        return (
                            schedule_comparison_result["total_hours_compared"]
                            == schedule_comparison_result["total_hours_matched"]
                        )
