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
from rct229.schema.config import ureg
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_8,
]
REQUIRED_DESIGN_ELEC_POWER_DESIGN_AIRFLOW_RATIO = 0.35 * ureg("W/cfm")


class PRM9012019Rule98g04(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012019Rule98g04, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule98g04.TerminalRule(),
            index_rmd=BASELINE_0,
            id="23-6",
            description="For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall be sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate and shall be modeled with 0.35 W/cfm fan power.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].zones[*].terminals[*]",
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
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return (
            context_item.BASELINE_0[
                "served_by_heating_ventilating_air_conditioning_system"
            ]
            in applicable_hvac_sys_ids
        )

    class TerminalRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule98g04.TerminalRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["primary_airflow", "fan"],
                    "fan": [
                        "design_airflow",
                        "design_electric_power",
                    ],
                },
                precision={
                    "design_airflow_b": {
                        "precision": 0.1,
                        "unit": "cfm",
                    },
                    "design_electric_power_b/design_airflow_b": {
                        "precision": 0.01,
                        "unit": "W/cfm",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            terminal_b = context.BASELINE_0
            design_airflow_b = terminal_b["fan"]["design_airflow"]
            primary_airflow_b = terminal_b["primary_airflow"]
            design_electric_power_b = terminal_b["fan"]["design_electric_power"]

            return {
                "design_airflow_b": CalcQ("air_flow_rate", design_airflow_b),
                "primary_airflow_b": CalcQ("air_flow_rate", primary_airflow_b),
                "design_electric_power_b": CalcQ(
                    "electric_power", design_electric_power_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            design_airflow_b = calc_vals["design_airflow_b"]
            primary_airflow_b = calc_vals["primary_airflow_b"]
            design_electric_power_b = calc_vals["design_electric_power_b"]

            return self.precision_comparison["design_airflow_b"](
                design_airflow_b,
                0.5 * primary_airflow_b,
            ) and self.precision_comparison["design_electric_power_b/design_airflow_b"](
                design_electric_power_b / design_airflow_b,
                REQUIRED_DESIGN_ELEC_POWER_DESIGN_AIRFLOW_RATIO,
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            design_airflow_b = calc_vals["design_airflow_b"]
            primary_airflow_b = calc_vals["primary_airflow_b"]
            design_electric_power_b = calc_vals["design_electric_power_b"]

            return std_equal(design_airflow_b, 0.5 * primary_airflow_b) and std_equal(
                design_electric_power_b / design_airflow_b, 0.35 * ureg("W/cfm")
            )
