from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_target_baseline_system import (
    SYSTEMORIGIN,
    get_zone_target_baseline_system,
)


class PRM9012019Rule00u91(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 5 (HVAC - System Zone Assignment)"""

    def __init__(self):
        super(PRM9012019Rule00u91, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule00u91.RuleModelDescriptionRule(),
            index_rmd=BASELINE_0,
            id="18-3",
            description="The lab exhaust fan shall be modeled as constant horsepower (kilowatts) reflecting constant-volume stack discharge with outdoor air bypass in the baseline",
            ruleset_section_title="HVAC",
            standard_section="Section G3.1-10 HVAC Systems for the baseline building",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
        )

    class RuleModelDescriptionRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule00u91.RuleModelDescriptionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={
                    "$": ["weather"],
                    "weather": ["climate_zone"],
                },
            )

        def get_calc_vals(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            climate_zone_b = rmd_b["weather"]["climate_zone"]

            target_baseline_systems_b = get_zone_target_baseline_system(
                rmd_b, rmd_p, climate_zone_b
            )

            return {"target_baseline_systems_b": target_baseline_systems_b}

        def applicability_check(self, context, calc_vals, data):
            target_baseline_systems_b = calc_vals["target_baseline_systems_b"]

            return any(
                [
                    target_baseline_systems_b[zone_id_b]["system_origin"]
                    == SYSTEMORIGIN.G311D
                    for zone_id_b in target_baseline_systems_b
                ]
            )
