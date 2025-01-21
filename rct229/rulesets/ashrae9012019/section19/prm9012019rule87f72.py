from pydash import flatten
from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_cooling import (
    get_proposed_hvac_modeled_with_virtual_cooling,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_heating import (
    get_proposed_hvac_modeled_with_virtual_heating,
)
from rct229.utils.assertions import getattr_


class PRM9012019Rule87f72(RuleDefinitionListIndexedBase):
    """Rule 34 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule87f72, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule87f72.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-34",
            description="Where no heating and/or cooling system is to be installed, and a heating or cooling system is being simulated only to meet the requirements described in this table, "
            "heating and/or cooling system fans shall not be simulated as running continuously during occupied hours but shall be cycled ON and OFF to meet heating and cooling loads during all hours in the baseline design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules Exception #1.",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_u = context.USER
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        HVAC_systems_virtual_cooling_list_p = (
            get_proposed_hvac_modeled_with_virtual_cooling(rmd_u, rmd_p)
        )
        HVAC_systems_virtual_heating_list_p = (
            get_proposed_hvac_modeled_with_virtual_heating(rmd_u, rmd_p)
        )

        HVAC_systems_virtual_list_p = list(
            set(
                HVAC_systems_virtual_cooling_list_p
                + HVAC_systems_virtual_heating_list_p
            )
        )

        hvac_sys_zones_served_dict_p = get_hvac_zone_list_w_area_by_rmd_dict(rmd_p)

        zones_virtual_heating_cooling_list = list(
            set(
                flatten(
                    [
                        hvac_sys_zones_served_dict_p[hvac_id_p]["zone_list"]
                        for hvac_id_p in HVAC_systems_virtual_list_p
                    ]
                )
            )
        )

        applicable_hvac_with_virtual_heating_cooling_b = list(
            set(
                flatten(
                    [
                        get_list_hvac_systems_associated_with_zone(rmd_b, zone_id_p)
                        for zone_id_p in zones_virtual_heating_cooling_list
                    ]
                )
            )
        )

        return {
            "applicable_hvac_with_virtual_heating_cooling_b": applicable_hvac_with_virtual_heating_cooling_b
        }

    class HVACRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule87f72.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def applicability_check(self, context, calc_vals, data):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            applicable_hvac_with_virtual_heating_cooling_b = data[
                "applicable_hvac_with_virtual_heating_cooling_b"
            ]

            return hvac_id_b in applicable_hvac_with_virtual_heating_cooling_b

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            operation_during_occupied_b = getattr_(
                hvac_b, "HVAC", "fan_system", "operation_during_occupied"
            )

            return (
                f"It appears that {hvac_id_b} is only being simulated in the proposed model to meet the requirements described in Section G3.1-10 HVAC Systems proposed column c and d for heating and/or cooling. "
                f"Check that the hvac system fan is simulated to be cycled ON and OFF to meet heating and/or cooling loads during occupied hours as applicable. "
                f"Note that per the RMD, the fan associated with {hvac_id_b} is operating as {operation_during_occupied_b} during occupied hours. "
                f"This may require further investigation if only heating or cooling is being simulated to meet Section G3.1-10 HVAC Systems proposed column c or d because different fan operation will be required depending on whether the system is operating in heating or cooling mode."
            )
