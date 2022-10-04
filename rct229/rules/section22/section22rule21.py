from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg

APPLICABLE_SYS_TYPES = [
    "SYS-7",
    "SYS-8",
    "SYS-11.1",
    "SYS-11.2",
    "SYS-12",
    "SYS-13",
    "SYS-7B",
    "SYS-8B",
    "SYS-11B",
    "SYS-12B",
    "SYS-13B",
]


class Section22Rule21(RuleDefinitionListIndexedBase):
    """Rule 21 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule21, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule21.ChillerRule(),
            index_rmr="baseline",
            id="22-21",
            description="The baseline building design’s chiller plant shall be modeled with chillers having the type as indicated in Table G3.1.3.7 as a function of building peak cooling load.",
            rmr_context="ruleset_model_instances/0",
            list_path="chillers[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11-a": ["hvac_sys_11_a"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        building_peak_load_b = 1
        target_chiller_type = (
            "SCREW" if building_peak_load_b < 600 * ureg("Btu/hr") else "CENTRIFUGAL"
        )
        return {"target_chiller_type": target_chiller_type}

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule21.ChillerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["compressor_type"],
                },
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.baseline
            compressor_type = chiller_b["compressor_type"]
            return {"compressor_type": compressor_type}

        def rule_check(self, context, calc_vals=None, data=None):
            compressor_type = calc_vals["compressor_type"]
            target_chiller_type = data["target_chiller_type"]
            return compressor_type == target_chiller_type
