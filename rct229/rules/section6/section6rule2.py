from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_9_6_1_fns import table_9_6_1_lookup
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals

GUEST_ROOM = schema_enums["LightingSpaceOptions2019ASHRAE901TG37"].GUEST_ROOM
DORMITORY_LIVING_QUARTERS = schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
].DORMITORY_LIVING_QUARTERS
DWELLING_UNIT = schema_enums["LightingSpaceOptions2019ASHRAE901TG37"].DWELLING_UNIT


class Section6Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule2, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section6Rule2.SpaceRule(),
            index_rmr="proposed",
            id="6-2",
            description="Spaces in proposed building with hardwired lighting, including Hotel/Motel Guest Rooms, "
            "Dormitory Living Quarters, Interior Lighting Power >= Table 9.6.1 or the lighting design in "
            "the user model, whichever is greater; For Dwelling Units, Interior Lighting Power >= "
            "0.6W/sq.ft. or the lighting design in the user model, whichever is greater",
            list_path="ruleset_model_instances[0].buildings[*].zones[*].spaces[*]",
        )

    class SpaceRule(RuleDefinitionBase):
        def __init__(self):
            super(Section6Rule2.SpaceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, True),
                required_fields={
                    "$": ["lighting_space_type", "interior_lighting"],
                    "interior_lighting": ["power_per_area"],
                },
            )

        def is_applicable(self, context, data=None):
            space_p = context.proposed
            lighting_space_type_p = space_p["lighting_space_type"]
            return lighting_space_type_p in [
                GUEST_ROOM,
                DWELLING_UNIT,
                DORMITORY_LIVING_QUARTERS,
            ]

        def get_calc_vals(self, context, data=None):
            space_p = context.proposed
            space_u = context.user

            # get allowance
            lighting_power_allowance_p = table_9_6_1_lookup(
                space_p["lighting_space_type"]
            )

            # sum of space_p lighting power density
            space_lighting_power_per_area_p = sum(
                interior_lighting["power_per_area"]
                for interior_lighting in space_p["interior_lighting"]
            )
            space_lighting_power_per_area_u = sum(
                interior_lighting["power_per_area"]
                for interior_lighting in space_u["interior_lighting"]
            )

            return {
                "lighting_power_allowance_p": lighting_power_allowance_p,
                "space_lighting_power_per_area_p": space_lighting_power_per_area_p,
                "space_lighting_power_per_area_u": space_lighting_power_per_area_u,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            lighting_power_allowance_p = calc_vals["lighting_power_allowance_p"]
            space_lighting_power_per_area_p = calc_vals[
                "space_lighting_power_per_area_p"
            ]
            space_lighting_power_per_area_u = calc_vals[
                "space_lighting_power_per_area_u"
            ]

            return space_lighting_power_per_area_p == max(
                lighting_power_allowance_p, space_lighting_power_per_area_u
            )
