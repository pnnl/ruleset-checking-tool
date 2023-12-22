from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_3_1_3_11_fns import (
    table_3_1_3_11_lookup,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import assert_
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
]


class Section22Rule20(RuleDefinitionListIndexedBase):
    """Rule 20 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule20, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section22Rule20.HeatRejectionRule(),
            index_rmr=BASELINE_0,
            id="22-20",
            description="The baseline minimum condenser water reset temperature is per Table G3.1.3.11.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.11 Heat Rejection (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].heat_rejections[*]",
            required_fields={
                "$": ["ruleset_model_descriptions", "weather"],
            },
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        assert_(
            rmd_b,
            "ruleset_model_instance list is empty",
        )
        rmi_b = rmd_b["ruleset_model_descriptions"][0]
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list containing all HVAC systems that are modeled in the rmi_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule20.HeatRejectionRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["leaving_water_setpoint_temperature"],
                },
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0

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
