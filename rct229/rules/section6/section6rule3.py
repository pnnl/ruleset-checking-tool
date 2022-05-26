from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_9_6_1_fns import table_9_6_1_lookup
from rct229.rule_engine.rule_base import RuleDefinitionListIndexedBase, RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals

GUEST_ROOM = schema_enums["LightingSpaceType2019ASHRAE901TG37"].GUEST_ROOM.name
DORMITORY_LIVING_QUARTERS = schema_enums["LightingSpaceType2019ASHRAE901TG37"].DORMITORY_LIVING_QUARTERS.name
DWELLING_UNITS = schema_enums["LightingSpaceType2019ASHRAE901TG37"].DWELLING_UNIT.name

class Section6Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule3, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, True, False),
            each_rule=Section6Rule3.SpaceRule(),
            index_rmr="proposed",
            id="6-3",
            description="Spaces in proposed building with hardwired lighting, including Hotel/Motel Guest Rooms, Dormitory Living Quarters, Interior Lighting Power >= Table 9.6.1; For Dwelling Units, Interior Lighting Power >= 0.6W/sq.ft.",
            list_path="ruleset_model_instances[0].buildings[*].zones[*].spaces[*]"
        )

    class SpaceRule(RuleDefinitionBase):
        def __init__(self):
            super(Section6Rule3.SpaceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, True, False),
                required_fields={
                    "$": ["lighting_space_type", "interior_lighting"],
                    "interior_lighting": ["power_per_area"],
                },
            )

        def is_applicable(self, context, data=None):
            space_p = context.proposed
            lighting_space_type_p = space_p["lighting_space_type"]
            return lighting_space_type_p in [GUEST_ROOM, DWELLING_UNITS, DORMITORY_LIVING_QUARTERS]

        def get_calc_vals(self, context, data=None):
            space_p = context.proposed
            space_u = context.user

            # get allowance
            lighting_power_allowance_p = table_9_6_1_lookup(space_p["lighting_space_type"])

            # sum of space_p lighting power density
            interior_lighting_space_p = sum(interior_lighting["power_per_area"] for interior_lighting in space_p["interior_lighting"])
            interior_lighting_space_u = sum(interior_lighting["power_per_area"] for interior_lighting in space_u["interior_lighting"])

            return {
                "lighting_power_allowance_p": lighting_power_allowance_p,
                "interior_lighting_space_p": interior_lighting_space_p,
                "interior_lighting_space_u": interior_lighting_space_u
            }

        def rule_check(self, context, calc_vals=None, data=None):
            lighting_power_allowance_p = calc_vals["lighting_power_allowance_p"]
            interior_lighting_space_p = calc_vals["interior_lighting_space_p"]
            interior_lighting_space_u = calc_vals["interior_lighting_space_u"]

            return interior_lighting_space_p == max(lighting_power_allowance_p, interior_lighting_space_u)

