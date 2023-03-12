from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals


MAX_COINCIDENT_UNMET_LOAD_HOUR = 300
MAX_SUM_HEATING_COOLING_UNMET_HOUR = 300
UNDETERMINED_MSG = "Conduct manual check that unmet load hours for the proposed design do not exceed 300 (of the 8760 hours simulated)."


class Section19Rule5(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule5, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section19Rule5.OutputRule(),
            index_rmr="proposed",
            id="19-5",
            description="Unmet load hours for the proposed design shall not exceed 300 (of the 8760 hours simulated).",
            ruleset_section_title="HVAC - General",
            standard_section=" Section G3.1.2.3",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].output[*]",
        )

    class OutputRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule5.OutputRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
                manual_check_required_msg=UNDETERMINED_MSG,
            )

        def get_calc_vals(self, context, data=None):
            output_p = context.baseline

            unmet_load_hours_heating_p = output_p["OutputInstance"][
                "unmet_load_hours_heating"
            ]
            unmet_load_hours_cooling_p = output_p["OutputInstance"][
                "unmet_load_hours_cooling"
            ]
            coincident_unmet_load_hours_p = output_p["OutputInstance"][
                "unmet_load_hours"
            ]

            return {
                "unmet_load_hours_heating_p": unmet_load_hours_heating_p,
                "unmet_load_hours_cooling_p": unmet_load_hours_cooling_p,
                "coincident_unmet_load_hours_p": coincident_unmet_load_hours_p,
            }

        def manual_check_required(self, context, calc_vals, data=None):
            unmet_load_hours_heating_p = calc_vals["unmet_load_hours_heating_p"]
            unmet_load_hours_cooling_p = calc_vals["unmet_load_hours_cooling_p"]
            coincident_unmet_load_hours_p = calc_vals["coincident_unmet_load_hours_p"]

            return not (
                coincident_unmet_load_hours_p <= MAX_COINCIDENT_UNMET_LOAD_HOUR
                or (
                    unmet_load_hours_heating_p + unmet_load_hours_cooling_p
                    <= MAX_SUM_HEATING_COOLING_UNMET_HOUR
                )
            )

        def rule_check(self, context, calc_vals=None, data=None):
            unmet_load_hours_heating_p = calc_vals["unmet_load_hours_heating_p"]
            unmet_load_hours_cooling_p = calc_vals["unmet_load_hours_cooling_p"]
            coincident_unmet_load_hours_p = calc_vals["coincident_unmet_load_hours_p"]

            return coincident_unmet_load_hours_p <= MAX_COINCIDENT_UNMET_LOAD_HOUR or (
                unmet_load_hours_heating_p + unmet_load_hours_cooling_p
                <= MAX_SUM_HEATING_COOLING_UNMET_HOUR
            )
