from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import ZERO, CalcQ

FAN_SHAFT_POWER_FACTOR = 0.9
HEAT_REJ_EFF_LIMIT = 38.2 * ureg("gpm/hp")


class Section22Rule17(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule17, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section22Rule17.HeatRejectionRule(),
            index_rmr=BASELINE_0,
            id="22-17",
            description="The baseline heat rejection device shall have an efficiency of 38.2 gpm/hp.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=False,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.heat_rejections[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        return {"heat_rejection_loop_ids_b": heat_rejection_loop_ids_b}

    class HeatRejectionRule(PartialRuleDefinition):
        def __init__(self):
            super(Section22Rule17.HeatRejectionRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["loop", "rated_water_flowrate"],
                },
            )

        def is_applicable(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            heat_rejection_loop_ids_b = data["heat_rejection_loop_ids_b"]
            heat_rejection_loop_b = heat_rejection_b["loop"]

            return heat_rejection_loop_b in heat_rejection_loop_ids_b

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0

            fan_shaft_power_b = (
                heat_rejection_b["fan_shaft_power"]
                if heat_rejection_b.get("fan_shaft_power")
                else (
                    getattr_(
                        heat_rejection_b, "heat_rejections", "fan_motor_nameplate_power"
                    )
                    * FAN_SHAFT_POWER_FACTOR
                    * getattr_(
                        heat_rejection_b, "heat_rejections", "fan_motor_efficiency"
                    )
                )
            )

            rated_water_flowrate_b = heat_rejection_b["rated_water_flowrate"]
            heat_rejection_efficiency_b = (
                0.0
                if fan_shaft_power_b == ZERO.POWER
                else rated_water_flowrate_b / fan_shaft_power_b
            )

            return {
                "fan_shaft_power_b": CalcQ("electric_power", fan_shaft_power_b),
                "rated_water_flowrate_b": CalcQ(
                    "volumetric_flow_rate", rated_water_flowrate_b
                ),
                "heat_rejection_efficiency_b": heat_rejection_efficiency_b,
            }

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            heat_rejection_b = context.BASELINE_0

            additional_note_for_no_shaft_power_b = (
                ""
                if heat_rejection_b.get("fan_shaft_power")
                else (
                    f"*Note: The fan shaft power for {heat_rejection_b['id']} was not given. For this evaluation, the fan shaft power was calculated using a rule of thumb "
                    f"where fan_shaft_power = fan_motor_nameplate_power * {FAN_SHAFT_POWER_FACTOR} * fan_motor_efficiency."
                )
            )
            heat_rejection_efficiency_b = calc_vals["heat_rejection_efficiency_b"]
            heat_rejection_efficiency_in_gpm_per_hp_b = round(
                heat_rejection_efficiency_b.to(ureg("gpm/hp")).magnitude, 1
            )

            if HEAT_REJ_EFF_LIMIT == heat_rejection_efficiency_b:
                undetermined_msg = (
                    f"The project includes a cooling tower. We calculated the cooling tower efficiency to be correct at 38.2 gpm/hp. "
                    f"However, it was not possible to verify that the modeling inputs correspond to the rating conditions in Table 6.8.1-7. "
                    f"{additional_note_for_no_shaft_power_b}"
                )
            elif heat_rejection_efficiency_b > HEAT_REJ_EFF_LIMIT:
                undetermined_msg = (
                    f"The project includes a cooling tower. We calculated the cooling tower efficiency to be {heat_rejection_efficiency_in_gpm_per_hp_b}, "
                    f"which is greater than the required efficiency of 38.2 gpm/hp, "
                    f"resulting in a more stringent baseline. However, it was not possible to verify that the modeling inputs correspond to the rating conditions in Table 6.8.1-7. "
                    f"{additional_note_for_no_shaft_power_b}"
                )
            else:
                undetermined_msg = (
                    f"The project includes a cooling tower. We calculated the cooling tower efficiency to be {heat_rejection_efficiency_in_gpm_per_hp_b}, "
                    f"which is less than the required efficiency of 38.2 gpm / hp.  However, it was not possible to verify that the modeling inputs correspond to the rating conditions in Table 6.8.1-7. "
                    f"Please review the efficiency and ensure that it is correct at the rating conditions as specified in the Table 6.8.1-7. {additional_note_for_no_shaft_power_b}"
                )

            return undetermined_msg

        def rule_check(self, context, calc_vals=None, data=None):
            return True
