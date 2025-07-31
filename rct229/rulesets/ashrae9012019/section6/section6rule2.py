from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.data_fns.table_9_6_1_fns import table_9_6_1_lookup
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

GUEST_ROOM = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
].GUEST_ROOM
DORMITORY_LIVING_QUARTERS = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
].DORMITORY_LIVING_QUARTERS
DWELLING_UNIT = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
].DWELLING_UNIT

DWELLING_UNIT_MIN_LIGHTING_POWER_PER_AREA = 0.6 * ureg("W/ft2")


class PRM9012019Rule37d98(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule37d98, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule37d98.SpaceRule(),
            index_rmd=PROPOSED,
            id="6-2",
            description="Spaces in proposed building with hardwired lighting, including Hotel/Motel Guest Rooms, Dormitory Living Quarters, Interior Lighting Power >= Table 9.6.1; For Dwelling Units, Interior Lighting Power >= 0.6W/sq.ft.",
            ruleset_section_title="Lighting",
            standard_section="Table G3.1 Part 6 Lighting under Proposed Building Performance paragraph (e)",
            is_primary_rule=True,
            list_path="$.ruleset_model_descriptions[0].buildings[*].building_segments[*].zones[*].spaces[*]",
        )

    def list_filter(self, context_item, data=None):
        space_p = context_item.PROPOSED
        # skip spaces has no lighting_space_type
        lighting_space_type_p = space_p.get("lighting_space_type")

        return lighting_space_type_p in [
            GUEST_ROOM,
            DWELLING_UNIT,
            DORMITORY_LIVING_QUARTERS,
            None,
        ]

    class SpaceRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule37d98.SpaceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={
                    "$": ["interior_lighting"],
                    "interior_lighting[*]": ["power_per_area"],
                },
                precision={
                    "space_lighting_power_per_area_p": {
                        "precision": 0.01,
                        "unit": "W/ft2",
                    }
                },
            )

        def is_applicable(self, context, data=None):
            # Set space not applicable if no lighting space type
            space_p = context.PROPOSED
            return space_p.get("lighting_space_type") is not None

        def get_calc_vals(self, context, data=None):
            space_p = context.PROPOSED
            space_u = context.USER

            # get allowance
            if space_p["lighting_space_type"] in [
                GUEST_ROOM,
                DORMITORY_LIVING_QUARTERS,
            ]:
                lighting_power_allowance_p = table_9_6_1_lookup(
                    space_p["lighting_space_type"]
                )["lpd"]
            else:
                lighting_power_allowance_p = DWELLING_UNIT_MIN_LIGHTING_POWER_PER_AREA

            space_lighting_power_per_area_p = sum(
                find_all("$.interior_lighting[*].power_per_area", space_p),
                ZERO.POWER_PER_AREA,
            )
            space_lighting_power_per_area_u = sum(
                find_all("$.interior_lighting[*].power_per_area", space_u),
                ZERO.POWER_PER_AREA,
            )

            return {
                "lighting_power_allowance_p": CalcQ(
                    "power_density", lighting_power_allowance_p
                ),
                "space_lighting_power_per_area_p": CalcQ(
                    "power_density", space_lighting_power_per_area_p
                ),
                "space_lighting_power_per_area_u": CalcQ(
                    "power_density", space_lighting_power_per_area_u
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            lighting_power_allowance_p = calc_vals["lighting_power_allowance_p"]
            space_lighting_power_per_area_p = calc_vals[
                "space_lighting_power_per_area_p"
            ]
            space_lighting_power_per_area_u = calc_vals[
                "space_lighting_power_per_area_u"
            ]

            return self.precision_comparison["space_lighting_power_per_area_p"](
                space_lighting_power_per_area_p,
                max(lighting_power_allowance_p, space_lighting_power_per_area_u),
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            lighting_power_allowance_p = calc_vals["lighting_power_allowance_p"]
            space_lighting_power_per_area_p = calc_vals[
                "space_lighting_power_per_area_p"
            ]
            space_lighting_power_per_area_u = calc_vals[
                "space_lighting_power_per_area_u"
            ]

            return std_equal(
                space_lighting_power_per_area_p,
                max(lighting_power_allowance_p, space_lighting_power_per_area_u),
            )
