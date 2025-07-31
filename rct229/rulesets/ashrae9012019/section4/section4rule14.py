from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one
from rct229.utils.pint_utils import ZERO, CalcQ

LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
ENERGY_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]

REQ_EQUIP_POWER_DENSITY = 20 * ureg("W/ft2")


class PRM9012019Rule66c61(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 4 (Schedules Setpoints)"""

    def __init__(self):
        super(PRM9012019Rule66c61, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule66c61.SpaceRule(),
            index_rmd=PROPOSED,
            id="4-14",
            description="A computer room is defined as a room whose primary function is to house equipment for the processing and storage of electronic data and that has a design electronic data equipment power density exceeding 20 W/ft2 of conditioned floor area.",
            ruleset_section_title="Schedules Setpoints",
            standard_section="Section 3 Definitions",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].zones[*].spaces[*]",
            required_fields={"$": ["schedules"]},
        )

    def is_applicable(self, context, data=None):
        # not applicable if there are no spaces identified as computer room in the RMD
        rmd_p = context.PROPOSED
        spaces_p = find_all(
            f'$.buildings[*].building_segments[*].zones[*].spaces[*][?(@.lighting_space_type="{LIGHTING_SPACE.COMPUTER_ROOM}")]',
            rmd_p,
        )
        return spaces_p

    def create_data(self, context, data):
        rmd_p = context.PROPOSED
        return {"schedules_p": rmd_p["schedules"]}

    def list_filter(self, context_item, data):
        # filter out none computer rooms
        space_p = context_item.PROPOSED
        return space_p.get("lighting_space_type") == LIGHTING_SPACE.COMPUTER_ROOM

    class SpaceRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule66c61.SpaceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                fail_msg="The space has been classed as a computer room in terms of the lighting space type but the "
                "electronic data equipment power density does not appear to exceed 20 w/sf.",
            )

        def get_calc_vals(self, context, data=None):
            space_p = context.PROPOSED
            total_space_misc_wattage_including_multiplier_p = ZERO.POWER

            schedules_p = data["schedules_p"]
            floor_area_p = getattr_(space_p, "space", "floor_area")

            assert_(
                floor_area_p > ZERO.AREA, f"Space floor area is smaller or equal to 0."
            )
            # skip undetermined outcome for no misc equipment, the reasoning behind it is assuming that the room is
            # identified as a computer room but there is 0 EPD, will generate failed outcome in rule check.
            for misc_equip_p in find_all(f"$.miscellaneous_equipment[*]", space_p):
                if misc_equip_p.get("energy_type") == ENERGY_SOURCE.ELECTRICITY:
                    misc_equip_power_p = getattr_(
                        misc_equip_p, "miscellaneous_equipment", "power"
                    )
                    mis_multiplier_id_p = misc_equip_p.get("multiplier_schedule")

                    # default value, used when no schedule is present in the misc equipment
                    misc_multiplier_value_p = 1.0
                    if mis_multiplier_id_p:
                        multiplier_schedule_p = find_exactly_one(
                            f'$[*][?(@.id="{mis_multiplier_id_p}")]', schedules_p
                        )
                        misc_multiplier_value_p = max(
                            1.0,
                            max(
                                getattr_(
                                    multiplier_schedule_p, "schedule", "hourly_values"
                                )
                            ),
                        )

                    total_space_misc_wattage_including_multiplier_p += (
                        misc_equip_power_p * misc_multiplier_value_p
                    )
            return {
                "epd_p": CalcQ(
                    "power_density",
                    total_space_misc_wattage_including_multiplier_p / floor_area_p,
                )
            }

        def rule_check(self, context, calc_vals=None, data=None):
            epd_p = calc_vals["epd_p"]
            return epd_p > REQ_EQUIP_POWER_DENSITY
