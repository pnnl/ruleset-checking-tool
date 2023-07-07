from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
]


class Section23Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(Section23Rule3, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section23Rule3.TerminalRule(),
            index_rmr="baseline",
            id="23-3",
            description="System 5, 6, 7 and 8 minimum volume setpoint shall be 30% of zone peak airflow, minimum outdoor airflow, or rate required to comply with minium accreditation standards whichever is larger.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Section G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7) and Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$..terminals[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict.keys()
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict.keys()
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        return {"applicable_hvac_sys_ids": applicable_hvac_sys_ids}

    def list_filter(self, context_item, data):
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return (
            context_item.baseline[
                "served_by_heating_ventilating_air_conditioning_system"
            ]
            in applicable_hvac_sys_ids
        )

    class TerminalRule(RuleDefinitionBase):
        def __init__(self):
            super(Section23Rule3.TerminalRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": [
                        "minimum_airflow",
                        "minimum_outdoor_airflow",
                        "primary_airflow",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            terminal_b = context.baseline
            minimum_airflow_b = terminal_b["minimum_airflow"]
            primary_airflow_b = terminal_b["primary_airflow"]
            minimum_outdoor_airflow_b = terminal_b["minimum_outdoor_airflow"]

            return {
                "minimum_airflow_b": CalcQ("volumetric_flow_rate", minimum_airflow_b),
                "primary_airflow_b": CalcQ("volumetric_flow_rate", primary_airflow_b),
                "minimum_outdoor_airflow_b": CalcQ(
                    "volumetric_flow_rate", minimum_outdoor_airflow_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            minimum_airflow_b = calc_vals["minimum_airflow_b"]
            primary_airflow_b = calc_vals["primary_airflow_b"]
            minimum_outdoor_airflow_b = calc_vals["minimum_outdoor_airflow_b"]

            return std_equal(
                minimum_airflow_b,
                max(primary_airflow_b * 0.3, minimum_outdoor_airflow_b),
            )
