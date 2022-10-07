from rct229.data_fns.table_3_1_3_11_fns import table_3_1_3_11_lookup
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

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


class Section22Rule20(RuleDefinitionListIndexedBase):
    """Rule 20 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule20, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section22Rule20.HeatRejectionRule(),
            index_rmr="baseline",
            id="22-20",
            description="The baseline minimum condenser water reset temperature is per Table G3.1.3.11.",
            list_path="ruleset_model_instances[0].heat_rejections[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11.1": ["hvac_sys_11_1"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule20.HeatRejectionRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["leaving_water_setpoint_temperature"],
                },
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.baseline

            tower_leaving_temperature_b = table_3_1_3_11_lookup(data["climate_zone"])[
                "leaving_water_temperature"
            ]

            leaving_water_setpoint_temperature_b = heat_rejection_b[
                "leaving_water_setpoint_temperature"
            ]
            return {
                "tower_leaving_temperature_b": CalcQ(
                    "temperature", tower_leaving_temperature_b
                ),
                "leaving_water_setpoint_temperature_b": CalcQ(
                    "temperature", leaving_water_setpoint_temperature_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            tower_leaving_temperature_b = calc_vals["tower_leaving_temperature_b"]
            leaving_water_setpoint_temperature_b = calc_vals[
                "leaving_water_setpoint_temperature_b"
            ]
            return std_equal(
                tower_leaving_temperature_b.to(ureg.kelvin),
                leaving_water_setpoint_temperature_b.to(ureg.kelvin),
            )
