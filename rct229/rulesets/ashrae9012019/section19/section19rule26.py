from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

REQ_HEATING_OVERSIZING_FACTOR = 0.25
REQ_COOLING_OVERSIZING_FACTOR = 0.15


class Section19Rule26(RuleDefinitionBase):
    """Rule 26 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule26, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            id="19-26",
            description="HVAC fans shall remain on during unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours in the proposed design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules exception #2 for the proposed building and Section G3.1.2.4 Appendix G Section Reference: None",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
        )


    def is_applicable(self, context, data=None):
        rmi_p = context.proposed

    def get_calc_vals(self, context, data=None):
        hvac_b = context.baseline


        return True

    def rule_check(self, context, calc_vals=None, data=None):


        return True