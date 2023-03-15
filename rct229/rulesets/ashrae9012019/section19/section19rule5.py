from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_dict,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_one

MIN_OA_CFM = 3000 * ureg("cfm")
DEMAND_CONTROL_VENTILATION_CONTROL = schema_enums[
    "DemandControlVentilationControlOptions"
]


class Section19Rule5(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule5, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section19Rule5.HVACRule(),
            index_rmr="baseline",
            id="19-5",
            description="Demand control ventilation is modeled in the baseline design in systems with outdoor air capacity greater than 3000 cfm serving areas with an average occupant design capacity greater than 100 people per 1000 ft^2.",
            ruleset_section_title="HVAC - General",
            standard_section=" Section G3.1.2.5 Excetion #1",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        hvac_zone_list_w_area_dict_b = get_hvac_zone_list_w_area_dict(rmi_b)

        return {"hvac_zone_list_w_area_dict_b": get_hvac_zone_list_w_area_dict(rmi_b)}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule5.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            fan_system_b = hvac_b["fan_system"]

            hvac_zone_list_w_area_dict_b = data["hvac_zone_list_w_area_dict_b"]
            is_DCV_modeled_b = False
            avg_occ_density = 0.0
            hvac_min_OA_flow = fan_system_b["minimum_outdoor_airflow"]

            demand_control_ventilation_control_b = fan_system_b.get(
                "demand_control_ventilation_control"
            )

            if (
                not demand_control_ventilation_control_b
                and demand_control_ventilation_control_b
                != DEMAND_CONTROL_VENTILATION_CONTROL.NONE
            ):
                is_DCV_modeled_b = True
                if hvac_min_OA_flow > MIN_OA_CFM:
                    zone_list_b = hvac_zone_list_w_area_dict_b[hvac_id_b]["zone_list"]
                    hvac_area_b = hvac_zone_list_w_area_dict_b[hvac_id_b]["total_area"]
                    total_hvac_sys_occupants_b = 0.0

                    for zone_b in zone_list_b:
                        total_occ_num_across_spaces_b = 0.0
                        for space_b in zone_b["spaces"]:
                            max_number_occ_b = space_b["number_of_occupants"]
                            total_occ_num_across_spaces_b += max_number_occ_b

                        total_hvac_sys_occupants_b += total_occ_num_across_spaces_b

                        avg_occ_density = total_hvac_sys_occupants_b / hvac_area_b

            return {
                "hvac_min_OA_flow": hvac_min_OA_flow,
                "is_DCV_modeled_b": is_DCV_modeled_b,
                "avg_occ_density": avg_occ_density,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            hvac_min_OA_flow = calc_vals["hvac_min_OA_flow"]
            is_DCV_modeled_b = calc_vals["is_DCV_modeled_b"]
            avg_occ_density = calc_vals["avg_occ_density"]

            return (
                hvac_min_OA_flow > MIN_OA_CFM
                and avg_occ_density > 0.1
                and avg_occ_density
            ) or (
                hvac_min_OA_flow <= MIN_OA_CFM
                and avg_occ_density >= 0.1
                and not avg_occ_density
            )
