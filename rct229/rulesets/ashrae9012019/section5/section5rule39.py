from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.utils.jsonpath_utils import find_all, find_one


class Section5Rule39(RuleDefinitionBase):
    """Rule 39 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule39, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="5-39",
            description="It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through basement floors.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-14(b) Building Envelope Modeling Requirements for the Proposed design and Baseline",
            is_primary_rule=True,
            required_fields={
                "$": ["weather", "ruleset_model_descriptions"],
                "$.weather": ["ground_temperature_schedule"],
            },
        )

    def get_calc_vals(self, context, data=None):
        rpd = context.BASELINE_0
        ground_temperature_schedule = rpd["weather"]["ground_temperature_schedule"]
        has_ground_temperature_schedule = any(
            [
                schedule["id"] == ground_temperature_schedule
                for schedule in find_all(
                    "$.ruleset_model_descriptions[0].schedules[*]", rpd
                )
            ]
        )
        return {"has_ground_temperature_schedule": has_ground_temperature_schedule}

    def rule_check(self, context, calc_vals, data=None):
        has_ground_temperature_schedule = calc_vals["has_ground_temperature_schedule"]
        return has_ground_temperature_schedule
