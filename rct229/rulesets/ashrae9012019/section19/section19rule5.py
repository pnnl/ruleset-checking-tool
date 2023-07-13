from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg

MAX_COINCIDENT_UNMET_LOAD_HOUR = 300 * ureg("hr")
MAX_SUM_HEATING_COOLING_UNMET_HOUR = 300 * ureg("hr")
UNDETERMINED_MSG = "Conduct manual check that unmet load hours for the proposed design do not exceed 300 (of the 8760 hours simulated)."


class Section19Rule5(RuleDefinitionBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule5, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            id="19-5",
            description="Unmet load hours for the proposed design shall not exceed 300 (of the 8760 hours simulated).",
            ruleset_section_title="HVAC - General",
            standard_section=" Section G3.1.2.3",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            required_fields={
                "$": ["output"],
                "output": ["output_instance"],
                "output_instance": [
                    "unmet_load_hours_heating",
                    "unmet_load_hours_cooling",
                    "unmet_load_hours",
                ],
            },
            manual_check_required_msg=UNDETERMINED_MSG,
        )

    def get_calc_vals(self, context, data=None):
        rmi_p = context.proposed
        output_instance_p = rmi_p["output"]["output_instance"]

        unmet_load_hours_heating_p = output_instance_p["unmet_load_hours_heating"]
        unmet_load_hours_cooling_p = output_instance_p["unmet_load_hours_cooling"]
        coincident_unmet_load_hours_p = output_instance_p["unmet_load_hours"]

        return {
            "unmet_load_hours_heating_p": unmet_load_hours_heating_p,
            "unmet_load_hours_cooling_p": unmet_load_hours_cooling_p,
            "coincident_unmet_load_hours_p": coincident_unmet_load_hours_p,
        }

    def manual_check_required(self, context, calc_vals, data=None):
        unmet_load_hours_heating_p = calc_vals["unmet_load_hours_heating_p"]
        unmet_load_hours_cooling_p = calc_vals["unmet_load_hours_cooling_p"]
        coincident_unmet_load_hours_p = calc_vals["coincident_unmet_load_hours_p"]

        return coincident_unmet_load_hours_p is None and (
            unmet_load_hours_heating_p is None or unmet_load_hours_cooling_p is None
        )

    def rule_check(self, context, calc_vals=None, data=None):
        unmet_load_hours_heating_p = calc_vals["unmet_load_hours_heating_p"]
        unmet_load_hours_cooling_p = calc_vals["unmet_load_hours_cooling_p"]
        coincident_unmet_load_hours_p = calc_vals["coincident_unmet_load_hours_p"]

        return (
            coincident_unmet_load_hours_p is not None
            and coincident_unmet_load_hours_p <= MAX_COINCIDENT_UNMET_LOAD_HOUR
        ) or (
            # we are certain at this step, both unmet_load_hours_heating_p and unmet_load_hours_cooling_p can't be None
            unmet_load_hours_heating_p + unmet_load_hours_cooling_p
            <= MAX_SUM_HEATING_COOLING_UNMET_HOUR
        )
