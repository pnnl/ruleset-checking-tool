from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.schema.config import ureg
from rct229.utils.compare_standard_val import std_le

MAX_COINCIDENT_UNMET_LOAD_HOUR = 300 * ureg("hr")
MAX_SUM_HEATING_COOLING_UNMET_HOUR = 300 * ureg("hr")
UNDETERMINED_MSG = "Conduct manual check that unmet load hours for the baseline design do not exceed 300 (of the 8760 hours simulated)."


class PRM9012019Rule97a53(RuleDefinitionBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule97a53, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="19-6",
            description=" Unmet load hours for the baseline design shall not exceed 300 (of the 8760 hours simulated).",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.3",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            required_fields={
                "$": ["model_output"],
                "model_output": [
                    "unmet_load_hours_heating",
                    "unmet_load_hours_cooling",
                    "unmet_load_hours",
                ],
            },
            manual_check_required_msg=UNDETERMINED_MSG,
            precision={
                "coincident_unmet_load_hours_b": {"precision": 1, "unit": "hour"},
                "unmet_load_hours_heating_b + unmet_load_hours_cooling_b": {
                    "precision": 1,
                    "unit": "hour",
                },
            },
        )

    def get_calc_vals(self, context, data=None):
        rmd_b = context.BASELINE_0
        output_instance_b = rmd_b["model_output"]

        unmet_load_hours_heating_b = output_instance_b["unmet_load_hours_heating"]
        unmet_load_hours_cooling_b = output_instance_b["unmet_load_hours_cooling"]
        coincident_unmet_load_hours_b = output_instance_b["unmet_load_hours"]

        return {
            "unmet_load_hours_heating_b": unmet_load_hours_heating_b,
            "unmet_load_hours_cooling_b": unmet_load_hours_cooling_b,
            "coincident_unmet_load_hours_b": coincident_unmet_load_hours_b,
        }

    def manual_check_required(self, context, calc_vals, data=None):
        unmet_load_hours_heating_b = calc_vals["unmet_load_hours_heating_b"]
        unmet_load_hours_cooling_b = calc_vals["unmet_load_hours_cooling_b"]
        coincident_unmet_load_hours_b = calc_vals["coincident_unmet_load_hours_b"]

        return coincident_unmet_load_hours_b is None and (
            unmet_load_hours_heating_b is None or unmet_load_hours_cooling_b is None
        )

    def rule_check(self, context, calc_vals=None, data=None):
        unmet_load_hours_heating_b = calc_vals["unmet_load_hours_heating_b"]
        unmet_load_hours_cooling_b = calc_vals["unmet_load_hours_cooling_b"]
        coincident_unmet_load_hours_b = calc_vals["coincident_unmet_load_hours_b"]

        return (
            coincident_unmet_load_hours_b is not None
            and (
                coincident_unmet_load_hours_b < MAX_COINCIDENT_UNMET_LOAD_HOUR
                or self.precision_comparison["coincident_unmet_load_hours_b"](
                    coincident_unmet_load_hours_b,
                    MAX_COINCIDENT_UNMET_LOAD_HOUR,
                )
            )
        ) or (
            # we are certain at this step, both unmet_load_hours_heating_b and unmet_load_hours_cooling_b can't be None
            unmet_load_hours_heating_b + unmet_load_hours_cooling_b
            < MAX_SUM_HEATING_COOLING_UNMET_HOUR
            or self.precision_comparison[
                "unmet_load_hours_heating_b + unmet_load_hours_cooling_b"
            ](
                unmet_load_hours_heating_b + unmet_load_hours_cooling_b,
                MAX_SUM_HEATING_COOLING_UNMET_HOUR,
            )
        )

    def is_tolerance_fail(self, context, calc_vals=None, data=None):
        unmet_load_hours_heating_b = calc_vals["unmet_load_hours_heating_b"]
        unmet_load_hours_cooling_b = calc_vals["unmet_load_hours_cooling_b"]
        coincident_unmet_load_hours_b = calc_vals["coincident_unmet_load_hours_b"]

        return (
            coincident_unmet_load_hours_b is not None
            and (std_le(coincident_unmet_load_hours_b, MAX_COINCIDENT_UNMET_LOAD_HOUR))
        ) or (
            # we are certain at this step, both unmet_load_hours_heating_b and unmet_load_hours_cooling_b can't be None
            std_le(
                unmet_load_hours_heating_b + unmet_load_hours_cooling_b,
                MAX_SUM_HEATING_COOLING_UNMET_HOUR,
            )
        )
