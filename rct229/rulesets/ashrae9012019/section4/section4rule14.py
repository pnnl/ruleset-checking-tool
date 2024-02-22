from pydash import find
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ

LIGHTING_SPACE = SchemaEnums["LightingSpaceOptions2019ASHRAE901TG37"]
ENERGY_SOURCE = SchemaEnums["EnergySourceOptions"]

REQ_EQUIP_POWER_DENSITY = 20 * ureg("W/ft2")


class Section4Rule14(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 4 (Schedule-Setpoints)"""

    def __init__(self):
        super(Section4Rule14, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=Section4Rule14.SpaceRule(),
            index_rmr=PROPOSED,
            id="4-14",
            description="A computer room is defined as a room whose primary function is to house equipment for the processing and storage of electronic data and that has a design electronic data equipment power density exceeding 20 W/ft2 of conditioned floor area.",
            ruleset_section_title="Schedule - Setpoints",
            standard_section="Section 3 Definitions",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].zones[*].spaces[*]",
        )

    def create_data(self, context, data):
        rmd_p = context.proposed

        sch_ids_p = find_all(
            f'$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*][?(@.energy_type="ELECTRICITY")].multiplier_schedule',
            rmd_p,
        )
        schedule_p = []
        for scd_id_p in sch_ids_p:
            schedule_p += find_all(f'$.schedules[*][?(@id = "{scd_id_p}")]', rmd_p)

        return {"schedule_p": schedule_p}

    class SpaceRule(RuleDefinitionBase):
        def __init__(self):
            super(Section4Rule14.SpaceRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={
                    "$": [
                        "lighting_space_type",
                        "miscellaneous_equipment",
                        "floor_area",
                    ],
                },
                fail_msg="The space has been classed as a computer room in terms of the lighting space type but the electronic data equipment power density does not appear to exceed 20 w/sf.",
            )

        def get_calc_vals(self, context, data=None):
            space_p = context.proposed

            schedule_p = data["schedule_p"]
            floor_area_p = space_p["floor_area"]

            total_space_misc_Wattage_including_multiplier_p = ZERO.POWER
            if space_p["lighting_space_type"] == LIGHTING_SPACE.COMPUTER_ROOM:
                for misc_equip_p in space_p["miscellaneous_equipment"]:
                    if misc_equip_p["energy_type"] == ENERGY_SOURCE.ELECTRICITY:
                        misc_equip_power_p = getattr_(
                            misc_equip_p, "miscellaneous_equipment", "power"
                        )
                        mis_multiplier_id_p = getattr_(
                            misc_equip_p,
                            "miscellaneous_equipment",
                            "multiplier_schedule",
                        )

                        total_space_misc_Wattage_including_multiplier_p += min(
                            1,
                            max(
                                misc_equip_power_p
                                * find(
                                    schedule_p,
                                    lambda d: d.get("id") == mis_multiplier_id_p,
                                )
                            ),
                        )

            EPD_p = total_space_misc_Wattage_including_multiplier_p / floor_area_p

            return {"EPD_p": CalcQ("power_density", EPD_p)}

        def rule_check(self, context, calc_vals=None, data=None):
            EPD_p = calc_vals["EPD_p"]

            return EPD_p > REQ_EQUIP_POWER_DENSITY
