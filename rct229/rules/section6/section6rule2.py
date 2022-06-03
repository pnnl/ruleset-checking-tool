from rct229.data_fns.table_G3_7_fns import table_G3_7_lookup
from rct229.data_fns.table_G3_8_fns import table_G3_8_lookup
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import pint_sum


class Section6Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule2, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section6Rule2.BuildingRule(),
            index_rmr="proposed",
            id="6-2",
            description="The total building interior lighting power shall not exceed the interior lighting power allowance determined using either Table G3.7 or G3.8",
            rmr_context="ruleset_model_instances/0/buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section6Rule2.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True)
            )

        def get_calc_vals(self, context, data=None):
            building_allowable_lighting_power = 0
            building_design_lighting_power = 0

            for building_segment in context.proposed["building_segments"]:
                building_segment_floor_area = 0
                building_segment_allowable_lighting_power = 0
                building_segment_design_lighting_power = 0

                building_segment_lighting_building_area_type = building_segment[
                    "lighting_building_area_type"
                ]
                building_segment_uses_building_area_method = (
                    building_segment_lighting_building_area_type != "NONE"
                )

                for zone in find_all("$..zones[*]", building_segment):
                    zone_volume = zone["volume"]
                    zone_floor_area = pint_sum(find_all("$..floor_area", zone))
                    zone_avg_height = zone_volume / zone_floor_area

                    for space in zone["spaces"]:
                        space_floor_area = space["floor_area"]
                        space_design_lighting_power = (
                            pint_sum(
                                find_all("interior_lighting[*].power_per_area", space)
                            )
                            * space_floor_area
                        )
                        building_segment_design_lighting_power += (
                            space_design_lighting_power
                        )
                        if building_segment_uses_building_area_method:
                            building_segment_floor_area += space_floor_area
                        else:
                            # The building segment uses the Space-by-Space Method
                            lighting_space_type = space["lighting_space_type"]
                            space_allowable_lpd = table_G3_7_lookup(
                                lighting_space_type,
                                # do not need control type
                                None,
                                space_height=zone_avg_height,
                                space_area=space_floor_area
                            )["lpd"]
                            building_segment_allowable_lighting_power += (
                                space_allowable_lpd * space_floor_area
                            )

                if building_segment_uses_building_area_method:
                    building_segment_allowable_lpd = table_G3_8_lookup(
                        building_area_type=building_segment_lighting_building_area_type
                    )["lpd"]
                    building_segment_allowable_lighting_power = (
                        building_segment_allowable_lpd * building_segment_floor_area
                    )

                building_allowable_lighting_power += (
                    building_segment_allowable_lighting_power
                )
                building_design_lighting_power += building_segment_design_lighting_power

            return {
                "building_allowable_lighting_power": building_allowable_lighting_power,
                "building_design_lighting_power": building_design_lighting_power,
            }

        def rule_check(self, context, calc_vals, data=None):
            return (
                calc_vals["building_design_lighting_power"]
                <= calc_vals["building_allowable_lighting_power"]
            )
