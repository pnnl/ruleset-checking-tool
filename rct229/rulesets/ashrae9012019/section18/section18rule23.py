from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_target_baseline_system import (
    SYSTEMORIGIN,
    get_zone_target_baseline_system,
)


class Section18Rule23(RuleDefinitionListIndexedBase):
    """Rule 23 of ASHRAE 90.1-2019 Appendix G Section 5 (HVAC - System Zone Assignment)"""

    def __init__(self):
        super(Section18Rule23, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section18Rule23.RuleModelDescriptionRule(),
            index_rmr="baseline",
            id="18-23",
            description="The lab exhaust fan shall be modeled as constant horsepower (kilowatts) reflecting constant-volume stack discharge with outdoor air bypass in the baseline",
            ruleset_section_title="HVAC",
            standard_section="Section G3.1-10 HVAC Systems for the baseline building",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions/0",
            required_fields={
                "$": ["calendar", "weather"],
                "$.weather": ["climate_zone"],
                "$.calendar": ["is_leap_year"],
            },
            data_items={
                "climate_zone": ("baseline", "weather/climate_zone"),
                "is_leap_year": ("baseline", "calendar/is_leap_year"),
            },
        )

    class RuleModelDescriptionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section18Rule23.RuleModelDescriptionRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
            )

        def get_calc_vals(self, context, data=None):
            rmd_b = context.baseline
            rmd_p = context.proposed
            climate_zone_b = data["climate_zone"]
            is_leap_year_b = data["is_leap_year"]

            target_baseline_systems_b = get_zone_target_baseline_system(
                rmd_b, rmd_p, climate_zone_b, is_leap_year_b
            )

            return {"target_baseline_systems_b": target_baseline_systems_b}

        def rule_check(self, context, calc_vals, data=None):
            target_baseline_systems_b = calc_vals["target_baseline_systems_b"]

            return any(
                [
                    target_baseline_systems_b[zone_id_b] == SYSTEMORIGIN.G311D
                    for zone_id_b in target_baseline_systems_b
                ]
            )
