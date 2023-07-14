from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg

MAX_COINCIDENT_UNMET_LOAD_HOUR = 300 * ureg("hr")
MAX_SUM_HEATING_COOLING_UNMET_HOUR = 300 * ureg("hr")
UNDETERMINED_MSG = "Conduct manual check that unmet load hours for the baseline design do not exceed 300 (of the 8760 hours simulated)."


class Section19Rule6(RuleDefinitionBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule6, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            id="19-6",
            description=" Unmet load hours for the baseline design shall not exceed 300 (of the 8760 hours simulated).",
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
        rmi_b = context.baseline
        output_instance_b = rmi_b["output"]["output_instance"]

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
            and coincident_unmet_load_hours_b <= MAX_COINCIDENT_UNMET_LOAD_HOUR
        ) or (
            # we are certain at this step, both unmet_load_hours_heating_b and unmet_load_hours_cooling_b can't be None
            unmet_load_hours_heating_b + unmet_load_hours_cooling_b
            <= MAX_SUM_HEATING_COOLING_UNMET_HOUR
        )
