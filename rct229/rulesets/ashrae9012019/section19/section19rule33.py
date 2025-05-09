from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_cooling import (
    get_proposed_hvac_modeled_with_virtual_cooling,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_heating import (
    get_proposed_hvac_modeled_with_virtual_heating,
)
from rct229.utils.assertions import getattr_


class PRM9012019Rule28i68(RuleDefinitionListIndexedBase):
    """Rule 33 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule28i68, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule28i68.HVACRule(),
            index_rmd=PROPOSED,
            id="19-33",
            description="Where no heating and/or cooling system is to be installed, and a heating or cooling system is being simulated only to meet the requirements described in Section G3.1-10 HVAC Systems proposed column c and d, "
            "heating and/or cooling system fans shall simulated to be cycled ON and OFF to meet heating and cooling loads during occupied hours in the proposed design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-10 HVAC Systems proposed column c and d",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_u = context.USER
        rmd_p = context.PROPOSED
        applicable_HVAC_systems_cooling_list_p = (
            get_proposed_hvac_modeled_with_virtual_cooling(rmd_u, rmd_p)
        )
        applicable_HVAC_systems_heating_list_p = (
            get_proposed_hvac_modeled_with_virtual_heating(rmd_u, rmd_p)
        )

        applicable_HVAC_systems_list_p = list(
            set(
                (
                    applicable_HVAC_systems_cooling_list_p
                    + applicable_HVAC_systems_heating_list_p
                )
            )
        )

        return {"applicable_HVAC_systems_list_p": applicable_HVAC_systems_list_p}

    class HVACRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule28i68.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
            )

        def applicability_check(self, context, calc_vals, data):
            hvac_p = context.PROPOSED
            hvac_id_p = hvac_p["id"]
            applicable_HVAC_systems_list_p = data["applicable_HVAC_systems_list_p"]

            return hvac_id_p in applicable_HVAC_systems_list_p

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_p = context.PROPOSED
            hvac_id_p = hvac_p["id"]

            operation_during_occupied_p = getattr_(
                hvac_p, "HVAC", "fan_system", "operation_during_occupied"
            )

            return (
                f"It appears that {hvac_id_p} is only being simulated in the proposed model to meet the requirements described in Section G3.1-10 HVAC Systems proposed column c and d for heating and/or cooling. "
                f"Check that the heating and/or cooling system fans are simulated to be cycled ON and OFF to meet heating and/or cooling loads during occupied hours as applicable. "
                f"Note that per the RMD the fan associated with {hvac_p} is operating as {operation_during_occupied_p} during occupied hours. "
                f"This may require further investigation if only heating or cooling is being simulated to meet Section G3.1-10 HVAC Systems proposed column c or d because different fan operation will be required depending on whether the system is operating in heating or cooling mode. "
            )
