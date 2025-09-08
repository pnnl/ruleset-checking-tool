from rct229.rule_engine.rule_base import RuleDefinitionBase
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
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
]

VENT_THRESHOLD_FACTOR = 0.5


class PRM9012019Rule46w18(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012019Rule46w18, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule46w18.HVACRule(),
            index_rmd=BASELINE_0,
            id="23-9",
            description="System 11 Minimum volume setpoint shall be the largest of 50% of the maximum design airflow rate, the minimum ventilation airflow rate or the airflow required to comply with codes or accredidation standards.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Exception to G3.1.3.13",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        return any(
            [
                baseline_system_types_dict[system_type]
                and baseline_system_type_compare(
                    system_type, applicable_sys_type, False
                )
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        return {"applicable_hvac_sys_ids": applicable_hvac_sys_ids}

    def list_filter(self, context_item, data):
        hvac_sys_b = context_item.BASELINE_0
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return hvac_sys_b["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule46w18.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                },
                manual_check_required_msg="The minimum volume flowrate is greater than the maximum of the minimum "
                "ventilation flowrate and 50% of the maximum supply flow rate.  This is "
                "correct IF the minimum volume flowrate is equal to any airflow required to "
                "comply with codes or accredidation standards, the system passes, "
                "otherwise it fails.  We are not able to determine the airflow required to "
                "comply with codes or accreditation standards at this time.",
                pass_msg="The minimum volume flowrate is equal to the maximum of the minimum ventilation flowrate and "
                "50% of the maximum supply flow rate.  If any airflow required to comply with codes or "
                "accredidation standards is MORE than this value, the minimum volume airflow should be set "
                "to this value.  We are not able to determine the airflow required to comply with codes or "
                "accreditation standards at this time, please double check that there are no additional "
                "codes or accreditation standards in regards to airflow. ",
                precision={
                    "minimum_airflow_b": {
                        "precision": 1,
                        "unit": "cfm",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            fan_system_b = hvac_b["fan_system"]
            min_volume_flowrate_b = getattr_(
                fan_system_b, "FanSystem", "minimum_airflow"
            )
            min_ventilation_flowrate_b = getattr_(
                fan_system_b, "FanSystem", "minimum_outdoor_airflow"
            )
            max_supply_flowrate = sum(
                [
                    supply_fan.get("design_airflow", ZERO.FLOW)
                    for supply_fan in find_all("$.supply_fans[*]", fan_system_b)
                ]
            )

            return {
                "minimum_airflow": CalcQ("air_flow_rate", min_volume_flowrate_b),
                "minimum_ventilation_airflow": CalcQ(
                    "air_flow_rate", min_ventilation_flowrate_b
                ),
                "max_supply_airflow": CalcQ("air_flow_rate", max_supply_flowrate),
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            minimum_airflow_b = calc_vals["minimum_airflow"]
            minimum_ventilation_airflow_b = calc_vals["minimum_ventilation_airflow"]
            max_supply_airflow_b = calc_vals["max_supply_airflow"]

            return minimum_airflow_b > max(
                minimum_ventilation_airflow_b,
                VENT_THRESHOLD_FACTOR * max_supply_airflow_b,
            )

        def rule_check(self, context, calc_vals=None, data=None):
            minimum_airflow_b = calc_vals["minimum_airflow"]
            minimum_ventilation_airflow_b = calc_vals["minimum_ventilation_airflow"]
            max_supply_airflow_b = calc_vals["max_supply_airflow"]

            return self.precision_comparison["minimum_airflow_b"](
                minimum_airflow_b,
                max(
                    minimum_ventilation_airflow_b,
                    VENT_THRESHOLD_FACTOR * max_supply_airflow_b,
                ),
            )
