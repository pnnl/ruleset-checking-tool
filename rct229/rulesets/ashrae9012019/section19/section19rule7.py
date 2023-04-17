from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.aggregate_min_OA_schedule_across_zones import (
    aggregate_min_OA_schedule_across_zones,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_min_oa_cfm_sch_zone import (
    get_min_oa_cfm_sch_zone,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

LIGHTING_SPACE = schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]


class Section19Rule7(RuleDefinitionBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule7, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            id="19-7",
            description="Minimum ventilation system outdoor air intake flow shall be the same for the proposed design and baseline building design except when any of the 4 exceptions defined in Section G3.1.2.5 are met.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.5 and Exception 2",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        rmi_p = context.proposed

        dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi_b)
        )

        zone_OA_CFM_list_of_schedules_b = []
        zone_OA_CFM_list_of_schedules_p = []
        for hvac_id_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
            rmi_b,
        ):
            for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                hvac_id_b
            ]["zone_list"]:
                zone_OA_CFM_list_of_schedules_b.append(
                    get_min_oa_cfm_sch_zone(rmi_b, zone_id_b)
                )
                zone_OA_CFM_list_of_schedules_p.append(
                    get_min_oa_cfm_sch_zone(rmi_p, zone_id_b)
                )

                for terminal in find_all(
                    f'$.buildings[*].building_segments[*].zones[?(@.id == "{zone_id_b}")]',
                    rmi_b,
                ):
                    if getattr_(terminal, "Terminal", "has_demand_control_ventilation"):
                        was_DCV_modeled_proposed = True
                    if getattr_(
                        terminal,
                        "Terminal",
                        "served_by_heating_ventilating_air_conditioning_system",
                    ):
                        pass

        aggregated_min_OA_schedule_across_zones_b = (
            aggregate_min_OA_schedule_across_zones(
                rmi_b, zone_OA_CFM_list_of_schedules_b
            )
        )
        aggregated_min_OA_schedule_across_zones_p = (
            aggregate_min_OA_schedule_across_zones(
                rmi_p, zone_OA_CFM_list_of_schedules_p
            )
        )

        return {
            "dict_of_zones_and_terminal_units_served_by_hvac_sys_b": dict_of_zones_and_terminal_units_served_by_hvac_sys_b,
            "aggregated_min_OA_schedule_across_zones_b": aggregated_min_OA_schedule_across_zones_b,
            "aggregated_min_OA_schedule_across_zones_p": aggregated_min_OA_schedule_across_zones_p,
        }

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        dict_of_zones_and_terminal_units_served_by_hvac_sys_b = data[
            "dict_of_zones_and_terminal_units_served_by_hvac_sys_b"
        ]

        hvac_system_serves_only_labs = True
        all_lighting_space_types_defined = True
        for hvac_id_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
            rmi_b,
        ):
            for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                hvac_id_b
            ]["zone_list"]:
                for space in find_all(
                    f'$.buildings[*].building_segments[*].zones[?(@.id == "{zone_id_b}")].spaces[*]',
                    rmi_b,
                ):
                    if hvac_system_serves_only_labs:
                        if space.get("lighting_space_type") is not None:
                            are_any_lighting_space_types_defined = True
                            if (
                                space.get("lighting_space_type")
                                != LIGHTING_SPACE.LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM
                            ):
                                hvac_system_serves_only_labs = False
                            else:
                                all_lighting_space_types_defined = False

        return not hvac_system_serves_only_labs or (
            hvac_system_serves_only_labs and not all_lighting_space_types_defined
        )

    def get_calc_vals(self, context, data=None):
        aggregated_min_OA_schedule_across_zones_b = data[
            "aggregated_min_OA_schedule_across_zones_b"
        ]
        aggregated_min_OA_schedule_across_zones_p = data[
            "aggregated_min_OA_schedule_across_zones_p"
        ]

        is_DCV_modeled_b = False
        is_DCV_modeled_p = False
        zone_air_distribution_effectiveness_greater_than_1 = False

        all_lighting_space_types_defined = True
        are_any_lighting_space_types_defined = False

        OA_CFM_schedule_match = (
            True
            if aggregated_min_OA_schedule_across_zones_b
            == aggregated_min_OA_schedule_across_zones_p
            else False
        )

        modeled_baseline_total_zone_min_OA_CFM = sum(
            aggregated_min_OA_schedule_across_zones_b
        )
        aggregated_min_OA_schedule_across_zones_p = sum(
            aggregated_min_OA_schedule_across_zones_p
        )

        return {
            "OA_CFM_schedule_match": OA_CFM_schedule_match,
            "modeled_baseline_total_zone_min_OA_CFM": modeled_baseline_total_zone_min_OA_CFM,
            "aggregated_min_OA_schedule_across_zones_p": aggregated_min_OA_schedule_across_zones_p,
        }

    def manual_check_required(self, context, calc_vals=None, data=None):
        modeled_baseline_total_zone_min_OA_CFM = data[
            "modeled_baseline_total_zone_min_OA_CFM"
        ]
        modeled_proposed_total_zone_min_OA_CFM = data[
            "modeled_proposed_total_zone_min_OA_CFM"
        ]
        zone_air_distribution_effectiveness_greater_than_1 = data[
            "zone_air_distribution_effectiveness_greater_than_1"
        ]

        return (
            True
            if (
                modeled_baseline_total_zone_min_OA_CFM
                > modeled_proposed_total_zone_min_OA_CFM
                and zone_air_distribution_effectiveness_greater_than_1
            )
            or (
                modeled_baseline_total_zone_min_OA_CFM
                < modeled_proposed_total_zone_min_OA_CFM
            )
            else False
        )

    def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
        hvac_id_b = calc_vals["hvac_id_b"]
        modeled_baseline_total_zone_min_OA_CFM = data[
            "modeled_baseline_total_zone_min_OA_CFM"
        ]
        modeled_proposed_total_zone_min_OA_CFM = data[
            "modeled_proposed_total_zone_min_OA_CFM"
        ]
        zone_air_distribution_effectiveness_greater_than_1 = data[
            "zone_air_distribution_effectiveness_greater_than_1"
        ]
        hvac_system_serves_only_labs = data["hvac_system_serves_only_labs"]

        if (
            modeled_baseline_total_zone_min_OA_CFM
            > modeled_proposed_total_zone_min_OA_CFM
            and zone_air_distribution_effectiveness_greater_than_1
        ):
            if hvac_system_serves_only_labs:
                # Case 7 msg
                undetermined_msg = f"For {hvac_id_b} the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. It appears as though G3.1.2.5 Exception 2 may be applicable because the air distribution effectiveness was modeled as greater than 1. Alternatively, the system may only serves lab spaces and G3.1.2.5 Exception 4 may be applicable. A manual check for these exceptions is recommended otherwise fail."
            else:
                # Case 6 msg
                undetermined_msg = f"For {hvac_id_b} the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. It appears as though G3.1.2.5 Exception 2 may be applicable. A manual check for this exception is recommended otherwise fail."
        elif (
            modeled_baseline_total_zone_min_OA_CFM
            < modeled_proposed_total_zone_min_OA_CFM
        ):
            # Case 8 msg
            undetermined_msg = f"For {hvac_id_b} the modeled minimum ventilation system outdoor air intake flow CFM is lower than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. Check if G3.1.2.5 Exception 3 is applicable. This exception states that where the minimum outdoor air intake flow in the proposed design is provided in excess of the amount required by the building code or the rating authority, the baseline building design shall be modeled to reflect the greater of that required by either the rating authority or the building code and will be less than the proposed design."

        return undetermined_msg

    def rule_check(self, context, calc_vals=None, data=None):
        OA_CFM_schedule_match = calc_vals["OA_CFM_schedule_match"]
        hvac_system_serves_only_labs = calc_vals["hvac_system_serves_only_labs"]
        are_any_lighting_space_types_defined = calc_vals[
            "are_any_lighting_space_types_defined"
        ]

        return (
            (OA_CFM_schedule_match and not hvac_system_serves_only_labs)
            and (
                OA_CFM_schedule_match
                and hvac_system_serves_only_labs
                and are_any_lighting_space_types_defined
            )
            and (OA_CFM_schedule_match and not are_any_lighting_space_types_defined)
        )

    def get_pass_msg(self, context, calc_vals=None, data=None):
        hvac_id_b = calc_vals["hvac_id_b"]
        OA_CFM_schedule_match = calc_vals["OA_CFM_schedule_match"]
        hvac_system_serves_only_labs = calc_vals["hvac_system_serves_only_labs"]
        are_any_lighting_space_types_defined = calc_vals[
            "are_any_lighting_space_types_defined"
        ]

        if OA_CFM_schedule_match:
            if hvac_system_serves_only_labs and are_any_lighting_space_types_defined:
                # Case 2 msg
                pass_msg = f"{hvac_id_b} passes this check unless it only serves labs. This hvac system serves some labs but it could not be determined from the RMD if it only serves labs. Outcome is UNDETERMINED if the HVAC system only serves lab spaces due to G3.1.2.5 Exception 4."

            elif not hvac_system_serves_only_labs:
                # Case 3 msg
                pass_msg = f"{hvac_id_b} passes this check unless it only serves lab spaces (no space types were defined in the RMD so this could not be determined). Outcome is UNDETERMINED if the HVAC system only serves lab spaces due to G3.1.2.5 Exception 4."

        return pass_msg

    def get_fail_msg(self, context, calc_vals=None, data=None):
        hvac_id_b = calc_vals["hvac_id_b"]
        modeled_baseline_total_zone_min_OA_CFM = data[
            "modeled_baseline_total_zone_min_OA_CFM"
        ]
        modeled_proposed_total_zone_min_OA_CFM = data[
            "modeled_proposed_total_zone_min_OA_CFM"
        ]
        was_DCV_modeled_baseline = data["was_DCV_modeled_baseline"]
        was_DCV_modeled_proposed = data["was_DCV_modeled_proposed"]
        zone_air_distribution_effectiveness_greater_than_1 = data[
            "zone_air_distribution_effectiveness_greater_than_1"
        ]
        hvac_system_serves_only_labs = data["hvac_system_serves_only_labs"]

        if (
            modeled_baseline_total_zone_min_OA_CFM
            > modeled_proposed_total_zone_min_OA_CFM
            and not was_DCV_modeled_baseline
            and was_DCV_modeled_proposed
            and not zone_air_distribution_effectiveness_greater_than_1
        ):
            if hvac_system_serves_only_labs:
                # Case 5 msg
                Fail_msg = f"For {hvac_id_b} the baseline modeled minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. Demand-controlled ventilation was modeled in the proposed and not the baseline model and demand-controlled ventilation may be double accounted for in the model (per the HVAC controls and via reduced OA CFM rates in the proposed). Alternatively, the hvac system may only serve labs in which case G3.1.2.5 Exception 4 may be applicable and leading to allowed higher modeled rates in the baseline."
            else:
                # Case 4 msg
                Fail_msg = f"For {hvac_id_b} the baseline modeled minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. Demand-controlled ventilation was modeled in the proposed and not the baseline model and demand-controlled ventilation may be double accounted for in the model (per the HVAC controls and via reduced OA CFM rates in the proposed)."

        elif not hvac_system_serves_only_labs:
            # Case 9 msg
            Fail_msg = f"For {hvac_id_b} the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design which does not meet the requirements of Section G3.1.2.5."

        else:
            # Case 10 msg
            Fail_msg = f"For {hvac_id_b} the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design which does not meet the requirements of Section G3.1.2.5. Fail unless the hvac system only serves labs and G3.1.2.5 Exception 4 is applicable."

        return Fail_msg
