from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class Section19Rule3(PartialRuleDefinition):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule3, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="19-3",
            description="Weather conditions used in sizing runs to determine baseline equipment capacities shall be based either on design days developed using 99.6% heating design temperatures and 1% dry-bulb and 1% wet-bulb cooling design temperatures.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2.1",
            is_primary_rule=False,
            rmr_context="ruleset_model_descriptions/0/",
        )

    def applicability_check(self, context, calc_vals, data):
        rmd_b = context.BASELINE_0
        weather_b = rmd_b["weather"]

        return weather_b.get("cooling_design_day_type") != - or  weather_b.get("heating_design_day_type")

    def manual_check_required(self, context, calc_vals=None, data=None):


        return

    def get_manual_check_required_msg(self, context, calc_vals=None, data=None):

        return