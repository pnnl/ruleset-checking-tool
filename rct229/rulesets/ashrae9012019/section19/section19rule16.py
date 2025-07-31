from pydash import find_key
from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_9,
    HVAC_SYS.SYS_10,
]
COOLING_SYSTEM = SchemaEnums.schema_enums["CoolingSystemOptions"]


class PRM9012019Rule04f07(RuleDefinitionListIndexedBase):
    """Rule 16 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule04f07, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule04f07.ZoneRule(),
            index_rmd=BASELINE_0,
            id="19-16",
            description="For zones served by baseline system types 9 & 10, if the proposed design includes a fan or fans sized and controlled to provide non-mechanical cooling, the baseline building design shall include a separate fan to provide nonmechanical cooling, sized and controlled the same as the proposed design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.8.2",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].zones[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        hvac_sys_repo_b = {
            zone_id_b: get_list_hvac_systems_associated_with_zone(rmd_b, zone_id_b)
            for zone_id_b in find_all(
                "$.buildings[*].building_segments[*].zones[*].id", rmd_b
            )
        }

        hvac_sys_repo_p = {
            zone_id_p: get_list_hvac_systems_associated_with_zone(rmd_p, zone_id_p)
            for zone_id_p in find_all(
                "$.buildings[*].building_segments[*].zones[*].id", rmd_p
            )
        }

        hvac_has_non_mech_cooling_list_p = [
            getattr_(hvac_p, "HVAC", "cooling_system", "type")
            == COOLING_SYSTEM.NON_MECHANICAL
            for hvac_p in find_all(
                "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
                rmd_p,
            )
        ]

        return {
            "baseline_system_types_dict": get_baseline_system_types(rmd_b),
            "hvac_sys_repo_b": hvac_sys_repo_b,
            "hvac_sys_repo_p": hvac_sys_repo_p,
            "hvac_has_non_mech_cooling_list_p": hvac_has_non_mech_cooling_list_p,
        }

    class ZoneRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule04f07.ZoneRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
            )

        def get_calc_vals(self, context, data=None):
            zone_b = context.BASELINE_0
            zone_p = context.PROPOSED

            zone_id_b = zone_b["id"]
            hvac_sys_list_b = data["hvac_sys_repo_b"][zone_id_b]

            hvac_has_non_mech_cooling_list_p = data["hvac_has_non_mech_cooling_list_p"]
            baseline_system_types_dict = data["baseline_system_types_dict"]

            hvac_has_non_mech_cooling = any(hvac_has_non_mech_cooling_list_p)

            zone_non_mechanical_cooling_fan_airflow_p = find_one(
                "$.non_mechanical_cooling_fan_airflow", zone_p
            )
            sys_types = [
                find_key(
                    baseline_system_types_dict, lambda base_sys: hvac_sys in base_sys
                )
                for hvac_sys in hvac_sys_list_b
            ]

            zone_served_by_sys_9_or_10 = any(
                [
                    baseline_system_type_compare(
                        system_type, applicable_sys_type, False
                    )
                    for system_type in sys_types
                    for applicable_sys_type in APPLICABLE_SYS_TYPES
                ]
            )

            return {
                "hvac_has_non_mech_cooling": hvac_has_non_mech_cooling,
                "zone_non_mechanical_cooling_fan_airflow_p ": zone_non_mechanical_cooling_fan_airflow_p,
                "zone_served_by_sys_9_or_10": zone_served_by_sys_9_or_10,
            }

        def applicability_check(self, context, calc_vals, data):
            hvac_has_non_mech_cooling = calc_vals["hvac_has_non_mech_cooling"]
            zone_served_by_sys_9_or_10 = calc_vals["zone_served_by_sys_9_or_10"]

            return hvac_has_non_mech_cooling and zone_served_by_sys_9_or_10

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            zone_p = context.PROPOSED
            zone_id_p = zone_p["id"]

            return (
                f"{zone_id_p} has non-mechanical cooling in the proposed design and the zone is served by either system 9 or 10 in the baseline, "
                "conduct a manual check that the baseline building design includes a separate fan to provide nonmechanical cooling, sized and controlled the same as the proposed design."
            )
