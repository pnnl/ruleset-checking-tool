from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_building_lab_zones_list import (
    get_building_lab_zones_list,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_building_total_lab_exhaust_from_zone_exhaust_fans import (
    get_building_total_lab_exhaust_from_zone_exhaust_fans,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_zone_likely_a_vestibule import (
    is_zone_likely_a_vestibule,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_target_baseline_system import (
    SYSTEMORIGIN,
    get_zone_target_baseline_system,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all

EXHAUST_AIRFLOW_15000 = 15000 * ureg("cfm")


class PRM9012019Rule77j55(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 18 (HVAC - System Zone Assignment)"""

    def __init__(self):
        super(PRM9012019Rule77j55, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule77j55.RMDRule(),
            index_rmd=BASELINE_0,
            id="18-1",
            description="HVAC system type selection is based on ASHRAE 90.1 G3.1.1 (a-h).",
            ruleset_section_title="HVAC - System Zone Assignment",
            standard_section="Table G3.1.1",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule77j55.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule77j55.RMDRule.ZoneRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*].zones[*]",
                required_fields={
                    "$": ["weather"],
                    "weather": ["climate_zone"],
                },
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            climate_zone_b = rmd_b["weather"]["climate_zone"]

            zone_target_baseline_system_dict_b = get_zone_target_baseline_system(
                rmd_b, rmd_p, climate_zone_b
            )

            return bool(zone_target_baseline_system_dict_b)

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            climate_zone_b = rmd_b["weather"]["climate_zone"]

            zone_target_baseline_system_dict_b = get_zone_target_baseline_system(
                rmd_b, rmd_p, climate_zone_b
            )
            baseline_hvac_system_dict_b = get_baseline_system_types(rmd_b)
            get_building_lab_zones_list_b = get_building_lab_zones_list(rmd_p)

            zone_ids_list_b = find_all(
                "$.buildings[*].building_segments[*].zones[*].id", rmd_b
            )
            hvac_systems_serving_zone_b = {
                zone_id_b: get_list_hvac_systems_associated_with_zone(rmd_b, zone_id_b)
                for zone_id_b in zone_ids_list_b
            }
            is_zone_likely_a_vestibule_b = {
                zone_id_b: is_zone_likely_a_vestibule(rmd_b, zone_id_b)
                for zone_id_b in zone_ids_list_b
            }
            building_total_lab_exhaust_p = (
                get_building_total_lab_exhaust_from_zone_exhaust_fans(rmd_p)
            )

            return {
                "zone_target_baseline_system_dict_b": zone_target_baseline_system_dict_b,
                "baseline_hvac_system_dict_b": baseline_hvac_system_dict_b,
                "get_building_lab_zones_list_b": get_building_lab_zones_list_b,
                "hvac_systems_serving_zone_b": hvac_systems_serving_zone_b,
                "is_zone_likely_a_vestibule_b": is_zone_likely_a_vestibule_b,
                "building_total_lab_exhaust_p": building_total_lab_exhaust_p,
            }

        def list_filter(self, context_item, data):
            zone_b = context_item.BASELINE_0
            zone_id_b = zone_b["id"]
            zone_target_baseline_system_dict_b = data[
                "zone_target_baseline_system_dict_b"
            ]

            return zone_id_b in zone_target_baseline_system_dict_b

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule77j55.RMDRule.ZoneRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    precision={
                        "building_total_lab_exhaust_p": {
                            "precision": 1,
                            "unit": "cfm",
                        },
                    },
                )

            def get_calc_vals(self, context, data=None):
                zone_b = context.BASELINE_0
                zone_id_b = zone_b["id"]

                expected_system_type_b = data["zone_target_baseline_system_dict_b"][
                    zone_id_b
                ]["expected_system_type"]
                hvac_systems_serving_zone_b = data["hvac_systems_serving_zone_b"][
                    zone_id_b
                ]
                hvac_system_types_b = {
                    system_type: system_list
                    for system_type, system_list in data[
                        "baseline_hvac_system_dict_b"
                    ].items()
                    if system_list
                }
                hvac_system_types_serving_zone_b = [
                    system_type_str
                    for system_type_str, system_list in data[
                        "baseline_hvac_system_dict_b"
                    ].items()
                    if any(
                        sys_b in system_list for sys_b in hvac_systems_serving_zone_b
                    )
                ]

                return {
                    "hvac_system_types_b": hvac_system_types_b,
                    "hvac_system_types_serving_zone_b": hvac_system_types_serving_zone_b,
                    "expected_system_type_b": expected_system_type_b,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                zone_b = context.BASELINE_0
                zone_id_b = zone_b["id"]
                is_zone_likely_a_vestibule_b = data["is_zone_likely_a_vestibule_b"]
                building_total_lab_exhaust_p = data["building_total_lab_exhaust_p"]

                system_origin_b = data["zone_target_baseline_system_dict_b"][zone_id_b][
                    "system_origin"
                ]

                is_undetermined = False
                if system_origin_b == SYSTEMORIGIN.G311D:
                    is_undetermined = (
                        building_total_lab_exhaust_p < EXHAUST_AIRFLOW_15000
                        or self.precision_comparison["building_total_lab_exhaust_p"](
                            building_total_lab_exhaust_p,
                            EXHAUST_AIRFLOW_15000,
                        )
                    )
                elif system_origin_b == SYSTEMORIGIN.G311E:
                    is_undetermined = is_zone_likely_a_vestibule_b[zone_id_b]

                return is_undetermined

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                zone_b = context.BASELINE_0
                zone_id_b = zone_b["id"]

                system_origin_b = data["zone_target_baseline_system_dict_b"][zone_id_b][
                    "system_origin"
                ]
                expected_system_type_b = data["zone_target_baseline_system_dict_b"][
                    zone_id_b
                ]["expected_system_type"]

                advisory_note = ""
                if system_origin_b == SYSTEMORIGIN.G311D:
                    advisory_note = (
                        f"HVAC system type {expected_system_type_b} was selected for this zone based on ASHRAE 90.1 Appendix G3.1.1.d, which reads: "
                        f"For laboratory spaces in a building having a total laboratory exhaust rate greater than 15,000 cfm, use a single system of type 5 or 7 serving only those spaces. "
                        f"We have determined that laboratory spaces in this building have a total exhaust greater than 15,000 cfm, but we cannot determine with certainty that at least 15,000cfm of the exhaust is dedicated to laboratory purposes. "
                        f"If the building laboratory exhaust is greater than 15,000cfm, the system type for this zone should be {expected_system_type_b}."
                    )

                elif system_origin_b == SYSTEMORIGIN.G311E:
                    advisory_note = (
                        f"HVAC system type {expected_system_type_b} was selected for this zone based on ASHRAE 90.1 Appendix G.3.1.1.e which reads: "
                        f"Thermal zones designed with heating-only systems in the proposed design serving storage rooms, stairwells, vestibules, electrical/mechanical rooms, "
                        f"and restrooms not exhausting or transferring air from mechanically cooled thermal zones in the proposed design shall use system type 9 or 10 in the baseline building design.` "
                        f"We expect that this space is a vestibule, but cannot make a determination with 100% accuracy. If the zone is one of the listed space types, then the system type should be {expected_system_type_b}."
                    )

                return advisory_note

            def rule_check(self, context, calc_vals=None, data=None):
                hvac_system_types_serving_zone_b = calc_vals[
                    "hvac_system_types_serving_zone_b"
                ]
                expected_system_type_b = calc_vals["expected_system_type_b"]

                return expected_system_type_b in hvac_system_types_serving_zone_b

            def get_fail_msg(self, context, calc_vals=None, data=None):
                zone_b = context.BASELINE_0
                zone_id_b = zone_b["id"]

                zone_target_baseline_system_dict_b = data[
                    "zone_target_baseline_system_dict_b"
                ][zone_id_b]
                system_type_origin_b = zone_target_baseline_system_dict_b[
                    "system_origin"
                ]
                expected_system_type_b = zone_target_baseline_system_dict_b[
                    "expected_system_type"
                ]

                return f"HVAC system type {expected_system_type_b} was selected based on {system_type_origin_b}."

            def get_pass_msg(self, context, calc_vals=None, data=None):
                zone_b = context.BASELINE_0
                zone_id_b = zone_b["id"]

                zone_target_baseline_system_dict_b = data[
                    "zone_target_baseline_system_dict_b"
                ][zone_id_b]
                system_type_origin_b = zone_target_baseline_system_dict_b[
                    "system_origin"
                ]
                expected_system_type_b = zone_target_baseline_system_dict_b[
                    "expected_system_type"
                ]

                return f"HVAC system type {expected_system_type_b} was selected based on {system_type_origin_b}."
