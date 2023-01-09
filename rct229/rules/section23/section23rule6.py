from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_6B,
    HVAC_SYS.SYS_8A,
    HVAC_SYS.SYS_8B,
]


class Section23Rule6(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(Section23Rule6, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section23Rule6.TerminalRule(),
            index_rmr="baseline",
            id="23-6",
            description="For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall be sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate and shall be modeled with 0.35 W/cfm fan power.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$..terminals[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # baseline_system_types_dict = get_baseline_system_types(rmi_b)
        baseline_system_types_dict = {
            "Sys-1": [],
            "Sys-10": [],
            "Sys-11b": [],
            "Sys-11.1": [],
            "Sys-11.1a": [],
            "Sys-11.1b": [],
            "Sys-11.1c": [],
            "Sys-11.2": [],
            "Sys-11.2a": [],
            "Sys-12": [],
            "Sys-12a": [],
            "Sys-12b": [],
            "Sys-12c": [],
            "Sys-13": [],
            "Sys-13a": [],
            "Sys-1a": [],
            "Sys-1b": [],
            "Sys-1c": [],
            "Sys-2": [],
            "Sys-3": [],
            "Sys-3a": [],
            "Sys-3b": [],
            "Sys-3c": [],
            "Sys-4": [],
            "Sys-5": [],
            "Sys-5b": [],
            "Sys-6": ["System 6"],
            "Sys-6b": [],
            "Sys-7": [],
            "Sys-7a": [],
            "Sys-7b": [],
            "Sys-7c": [],
            "Sys_8": [],
            "Sys_8a": [],
            "Sys-8b": [],
            "Sys-8c": [],
            "Sys-9": [],
            "Sys-9b": [],
        }
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_sys_types = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]

        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_sys_types
            ]
        )

    class TerminalRule(RuleDefinitionBase):
        def __init__(self):
            super(Section23Rule6.TerminalRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["primary_airflow"],
                    "fan": [
                        "design_airflow",
                        "design_electric_power",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            terminal_b = context.baseline
            design_airflow_b = terminal_b["fan"]["design_airflow"]
            primary_airflow_b = terminal_b["primary_airflow"]
            design_electric_power_b = terminal_b["fan"]["design_electric_power"]

            return {
                "design_airflow_b": CalcQ("volumetric_flow_rate_Ls", design_airflow_b),
                "primary_airflow_b": CalcQ(
                    "volumetric_flow_rate_Ls", primary_airflow_b
                ),
                "design_electric_power_b": CalcQ(
                    "electric_power", design_electric_power_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            design_airflow_b = calc_vals["design_airflow_b"]
            primary_airflow_b = calc_vals["primary_airflow_b"]
            design_electric_power_b = calc_vals["design_electric_power_b"]

            return std_equal(design_airflow_b, 0.5 * primary_airflow_b) and std_equal(
                design_electric_power_b.m, 0.35 * design_airflow_b.to("cfm").m
            )
