from rct229.data_fns.table_G3_4_fns import table_G34_lookup
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
            each_rule=Section22Rule20.HeatRejectionRule(),
            index_rmr="baseline",
            id="22-20",
            description="The baseline minimum condenser water reset temperature is per Table G3.1.3.11.",
            rmr_context="ruleset_model_instances/0",
            list_path="heat_rejections[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
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
        tower_leaving_temperature_b = data  ## should be updated
        return {"tower_leaving_temperature_b": tower_leaving_temperature_b}

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
            leaving_water_setpoint_temperature = heat_rejection_b[
                "leaving_water_setpoint_temperature"
            ]

            return {
                "leaving_water_setpoint_temperature": CalcQ(
                    "temperature", leaving_water_setpoint_temperature
                )
            }

        def rule_check(self, context, calc_vals=None, data=None):
            leaving_water_setpoint_temperature = calc_vals[
                "leaving_water_setpoint_temperature"
            ]
            tower_leaving_temperature_b = data["tower_leaving_temperature_b"]
            return std_equal(
                leaving_water_setpoint_temperature.to(ureg.kelvin),
                tower_leaving_temperature_b.to(ureg.kelvin),
            )
