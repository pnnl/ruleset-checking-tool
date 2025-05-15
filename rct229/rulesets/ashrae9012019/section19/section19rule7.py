from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.aggregate_min_OA_schedule_across_zones import (
    aggregate_min_OA_schedule_across_zones,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_min_oa_cfm_sch_zone import (
    get_min_oa_cfm_sch_zone,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.std_comparisons import std_equal
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
)

LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
DEMAND_CONTROL_VENTILATION_CONTROL = SchemaEnums.schema_enums[
    "DemandControlVentilationControlOptions"
]


class PRM9012019Rule29n92(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule29n92, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule29n92.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-7",
            description="Minimum ventilation system outdoor air intake flow shall be the same for the proposed design and baseline building design except when any of the 4 exceptions defined in Section G3.1.2.5 are met."
            "Exceptions included in this RDS: 2. When designing systems in accordance with Standard 62.1, Section 6.2, `Ventilation Rate Procedure,`"
            "reduced ventilation airflow rates may be calculated for each HVAC zone in the proposed design with a zone air distribution effectiveness (Ez) > 1.0 as defined by Standard 62.1, Table 6-2. "
            "Baseline ventilation airflow rates in those zones shall be calculated using the proposed design Ventilation Rate Procedure calculation with the following change only. Zone air distribution effectiveness shall be changed to (Ez) = 1.0 in each zone having a zone air distribution effectiveness (Ez) > 1.0. "
            "Proposed design and baseline build-ing design Ventilation Rate Procedure calculations, as described in Standard 62.1, shall be submitted to the rating authority to claim credit for this exception.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.5 and Exception 2",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
        )

        hvac_system_serves_only_labs = True
        are_any_lighting_space_types_defined = False
        all_lighting_space_types_defined = True
        for space_b in find_all(
            "$.buildings[*].building_segments[*].zones[*].spaces[*]",
            rmd_b,
        ):
            if hvac_system_serves_only_labs:
                lighting_space_type_b = space_b.get("lighting_space_type")
                if lighting_space_type_b is None:
                    all_lighting_space_types_defined = False
                else:
                    are_any_lighting_space_types_defined = True
                    if (
                        lighting_space_type_b
                        != LIGHTING_SPACE.LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM
                    ):
                        hvac_system_serves_only_labs = False
            else:
                all_lighting_space_types_defined = False

        zone_data = {}
        for hvac_id_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
            rmd_b,
        ):
            zone_data[hvac_id_b] = {
                "zone_OA_CFM_list_of_schedules_b": [],
                "zone_OA_CFM_list_of_schedules_p": [],
                "was_DCV_modeled_baseline": False,
                "was_DCV_modeled_proposed": False,
                "zone_air_distribution_effectiveness_greater_than_1": False,
            }
            for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                hvac_id_b
            ]["zone_list"]:
                zone_data[hvac_id_b]["zone_OA_CFM_list_of_schedules_b"].append(
                    get_min_oa_cfm_sch_zone(rmd_b, zone_id_b)
                )
                zone_data[hvac_id_b]["zone_OA_CFM_list_of_schedules_p"].append(
                    get_min_oa_cfm_sch_zone(rmd_p, zone_id_b)
                )

                # find if DCV was modeled in baseline
                zone_data[hvac_id_b]["was_DCV_modeled_baseline"] = any(
                    [
                        terminal_b.get("has_demand_control_ventilation", False)
                        for terminal_b in find_all(
                            "$.terminals[*]",
                            find_exactly_one_zone(rmd_b, zone_id_b),
                        )
                    ]
                )

                # find proposed zone
                zone_p = find_exactly_one_zone(rmd_p, zone_id_b)

                # find if DCV was modeled in proposed
                zone_data[hvac_id_b]["was_DCV_modeled_proposed"] = any(
                    [
                        terminal_p.get("has_demand_control_ventilation", False)
                        or find_one(
                            "$.fan_system.demand_control_ventilation_control",
                            (
                                find_exactly_one_hvac_system(
                                    rmd_p,
                                    getattr_(
                                        terminal_p,
                                        "terminals",
                                        "served_by_heating_ventilating_air_conditioning_system",
                                    ),
                                )
                            ),
                        )
                        not in [None, DEMAND_CONTROL_VENTILATION_CONTROL.NONE]
                        for terminal_p in find_all("$.terminals[*]", zone_p)
                    ]
                )

                # find if zone_air_distribution_effectiveness_greater_than_1 or not
                zone_data[hvac_id_b][
                    "zone_air_distribution_effectiveness_greater_than_1"
                ] = (
                    getattr_(
                        zone_p,
                        "zones",
                        "air_distribution_effectiveness",
                    )
                    > 1
                )

            zone_data[hvac_id_b][
                "aggregated_min_OA_schedule_across_zones_b"
            ] = aggregate_min_OA_schedule_across_zones(
                zone_data[hvac_id_b]["zone_OA_CFM_list_of_schedules_b"]
            )
            zone_data[hvac_id_b][
                "aggregated_min_OA_schedule_across_zones_p"
            ] = aggregate_min_OA_schedule_across_zones(
                zone_data[hvac_id_b]["zone_OA_CFM_list_of_schedules_p"]
            )

        return {
            "hvac_system_serves_only_labs": hvac_system_serves_only_labs,
            "are_any_lighting_space_types_defined": are_any_lighting_space_types_defined,
            "all_lighting_space_types_defined": all_lighting_space_types_defined,
            "zone_data": zone_data,
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule29n92.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                precision={
                    "aggregated_min_OA_schedule_across_zones_b": {
                        "precision": 1,
                        "unit": "cfm",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            hvac_system_serves_only_labs = data["hvac_system_serves_only_labs"]
            all_lighting_space_types_defined = data["all_lighting_space_types_defined"]

            return not hvac_system_serves_only_labs or (
                hvac_system_serves_only_labs and not all_lighting_space_types_defined
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            hvac_system_serves_only_labs = data["hvac_system_serves_only_labs"]
            are_any_lighting_space_types_defined = data[
                "are_any_lighting_space_types_defined"
            ]
            all_lighting_space_types_defined = data["all_lighting_space_types_defined"]

            zone_data = data["zone_data"][hvac_id_b]
            aggregated_min_OA_schedule_across_zones_b = zone_data[
                "aggregated_min_OA_schedule_across_zones_b"
            ]
            aggregated_min_OA_schedule_across_zones_p = zone_data[
                "aggregated_min_OA_schedule_across_zones_p"
            ]
            zone_air_distribution_effectiveness_greater_than_1 = zone_data[
                "zone_air_distribution_effectiveness_greater_than_1"
            ]

            OA_CFM_schedule_match = all(
                [
                    self.precision_comparison[
                        "aggregated_min_OA_schedule_across_zones_b"
                    ](
                        aggregated_min_OA_schedule_across_zones_b[i],
                        aggregated_min_OA_schedule_across_zones_p[i],
                    )
                    for i in range(len(aggregated_min_OA_schedule_across_zones_b))
                ]
            )

            modeled_baseline_total_zone_min_OA_CFM = sum(
                aggregated_min_OA_schedule_across_zones_b
            )
            modeled_proposed_total_zone_min_OA_CFM = sum(
                aggregated_min_OA_schedule_across_zones_p
            )

            was_DCV_modeled_baseline = zone_data["was_DCV_modeled_baseline"]
            was_DCV_modeled_proposed = zone_data["was_DCV_modeled_proposed"]

            return {
                "hvac_id_b": hvac_id_b,
                "hvac_system_serves_only_labs": hvac_system_serves_only_labs,
                "are_any_lighting_space_types_defined": are_any_lighting_space_types_defined,
                "all_lighting_space_types_defined": all_lighting_space_types_defined,
                "OA_CFM_schedule_match": OA_CFM_schedule_match,
                "zone_air_distribution_effectiveness_greater_than_1": zone_air_distribution_effectiveness_greater_than_1,
                "modeled_baseline_total_zone_min_OA_CFM": modeled_baseline_total_zone_min_OA_CFM,
                "modeled_proposed_total_zone_min_OA_CFM": modeled_proposed_total_zone_min_OA_CFM,
                "was_DCV_modeled_baseline": was_DCV_modeled_baseline,
                "was_DCV_modeled_proposed": was_DCV_modeled_proposed,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            OA_CFM_schedule_match = calc_vals["OA_CFM_schedule_match"]
            hvac_system_serves_only_labs = calc_vals["hvac_system_serves_only_labs"]
            are_any_lighting_space_types_defined = calc_vals[
                "are_any_lighting_space_types_defined"
            ]
            zone_air_distribution_effectiveness_greater_than_1 = calc_vals[
                "zone_air_distribution_effectiveness_greater_than_1"
            ]
            modeled_baseline_total_zone_min_OA_CFM = calc_vals[
                "modeled_baseline_total_zone_min_OA_CFM"
            ]
            modeled_proposed_total_zone_min_OA_CFM = calc_vals[
                "modeled_proposed_total_zone_min_OA_CFM"
            ]

            return (
                (
                    # Case 2
                    OA_CFM_schedule_match
                    and hvac_system_serves_only_labs
                    and are_any_lighting_space_types_defined
                )
                or (
                    # Case 6 & 7
                    modeled_baseline_total_zone_min_OA_CFM
                    > modeled_proposed_total_zone_min_OA_CFM
                    and zone_air_distribution_effectiveness_greater_than_1
                )
                or (
                    # Case 8
                    modeled_baseline_total_zone_min_OA_CFM
                    < modeled_proposed_total_zone_min_OA_CFM
                )
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_id_b = calc_vals["hvac_id_b"]

            OA_CFM_schedule_match = calc_vals["OA_CFM_schedule_match"]
            hvac_system_serves_only_labs = calc_vals["hvac_system_serves_only_labs"]
            are_any_lighting_space_types_defined = calc_vals[
                "are_any_lighting_space_types_defined"
            ]
            hvac_system_serves_only_labs = calc_vals["hvac_system_serves_only_labs"]
            modeled_baseline_total_zone_min_OA_CFM = calc_vals[
                "modeled_baseline_total_zone_min_OA_CFM"
            ]
            modeled_proposed_total_zone_min_OA_CFM = calc_vals[
                "modeled_proposed_total_zone_min_OA_CFM"
            ]

            if (
                OA_CFM_schedule_match
                and hvac_system_serves_only_labs
                and are_any_lighting_space_types_defined
            ):
                # Case 2
                undetermined_msg = (
                    f"{hvac_id_b} passes this check unless it only serves labs. This hvac system serves some labs but it could not be determined from the RMD "
                    f"if it only serves labs. Conduct manual check if the HVAC system only serves lab spaces due to G3.1.2.5 Exception 4."
                )
            elif (
                modeled_baseline_total_zone_min_OA_CFM
                > modeled_proposed_total_zone_min_OA_CFM
            ):
                if not hvac_system_serves_only_labs:
                    # Case 6
                    undetermined_msg = f"For {hvac_id_b} the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. It appears as though G3.1.2.5 Exception 2 may be applicable. A manual check for this exception is recommended otherwise fail."
                else:
                    # Case 7
                    undetermined_msg = f"For {hvac_id_b} the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. It appears as though G3.1.2.5 Exception 2 may be applicable because the air distribution effectiveness was modeled as greater than 1. Alternatively, the system may only serves lab spaces and G3.1.2.5 Exception 4 may be applicable. A manual check for these exceptions is recommended otherwise fail."

            else:
                # Case 8
                undetermined_msg = f"For {hvac_id_b} the modeled minimum ventilation system outdoor air intake flow CFM is lower than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. Check if G3.1.2.5 Exception 3 is applicable. This exception states that where the minimum outdoor air intake flow in the proposed design is provided in excess of the amount required by the building code or the rating authority, the baseline building design shall be modeled to reflect the greater of that required by either the rating authority or the building code and will be less than the proposed design."

            return undetermined_msg

        def rule_check(self, context, calc_vals=None, data=None):
            OA_CFM_schedule_match = calc_vals["OA_CFM_schedule_match"]

            return OA_CFM_schedule_match

        def get_pass_msg(self, context, calc_vals=None, data=None):
            hvac_id_b = calc_vals["hvac_id_b"]
            are_any_lighting_space_types_defined = calc_vals[
                "are_any_lighting_space_types_defined"
            ]

            pass_msg = ""
            if not are_any_lighting_space_types_defined:
                # Case 3
                pass_msg = (
                    f"{hvac_id_b} passes this check unless it only serves lab spaces (no space types were defined in the RMD so this could not be determined). "
                    f"Outcome is UNDETERMINED if the HVAC system only serves lab spaces due to G3.1.2.5 Exception 4."
                )

            return pass_msg

        def get_fail_msg(self, context, calc_vals=None, data=None):
            hvac_id_b = calc_vals["hvac_id_b"]
            hvac_system_serves_only_labs = calc_vals["hvac_system_serves_only_labs"]
            zone_air_distribution_effectiveness_greater_than_1 = calc_vals[
                "zone_air_distribution_effectiveness_greater_than_1"
            ]
            modeled_baseline_total_zone_min_OA_CFM = calc_vals[
                "modeled_baseline_total_zone_min_OA_CFM"
            ]
            modeled_proposed_total_zone_min_OA_CFM = calc_vals[
                "modeled_proposed_total_zone_min_OA_CFM"
            ]
            was_DCV_modeled_baseline = calc_vals["was_DCV_modeled_baseline"]
            was_DCV_modeled_proposed = calc_vals["was_DCV_modeled_proposed"]

            if (
                modeled_baseline_total_zone_min_OA_CFM
                > modeled_proposed_total_zone_min_OA_CFM
                and not was_DCV_modeled_baseline
                and was_DCV_modeled_proposed
                and not zone_air_distribution_effectiveness_greater_than_1
            ):
                if hvac_system_serves_only_labs:
                    # Case 5
                    Fail_msg = f"For {hvac_id_b} the baseline modeled minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. Demand-controlled ventilation was modeled in the proposed and not the baseline model and demand-controlled ventilation may be double accounted for in the model (per the HVAC controls and via reduced OA CFM rates in the proposed). Alternatively, the hvac system may only serve labs in which case G3.1.2.5 Exception 4 may be applicable and leading to allowed higher modeled rates in the baseline."
                else:
                    # Case 4
                    Fail_msg = f"For {hvac_id_b} the baseline modeled minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. Demand-controlled ventilation was modeled in the proposed and not the baseline model and demand-controlled ventilation may be double accounted for in the model (per the HVAC controls and via reduced OA CFM rates in the proposed)."

            elif not hvac_system_serves_only_labs:
                # Case 9
                Fail_msg = f"For {hvac_id_b} the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design which does not meet the requirements of Section G3.1.2.5."

            elif not std_equal(
                modeled_baseline_total_zone_min_OA_CFM,
                modeled_proposed_total_zone_min_OA_CFM,
            ):
                # Case 10
                Fail_msg = f"Fail because the outdoor air schedules do not appear to match between the baseline and proposed."

            else:
                # Case 11
                Fail_msg = f"For {hvac_id_b} the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design which does not meet the requirements of Section G3.1.2.5. Fail unless the hvac system only serves labs and G3.1.2.5 Exception 4 is applicable."

            return Fail_msg
