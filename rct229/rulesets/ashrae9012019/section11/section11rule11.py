from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value


class Section11Rule11(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule11, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule11.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-11",
            description=(
                "For buildings that will have no service water-heating loads, no service water-heating shall be "
                "modeled in baseline building model"
            ),
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, c",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionBase):
        def __init__(self):
            super(Section11Rule11.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
            )

        def is_applicable(self, context, data=None):
            rmd_p = context.PROPOSED
            swh_use_loads_p = sum(
                [
                    swh_use.get("use", 0.0)
                    # The json path needs to update if schema changes.
                    for building_segment in find_all(
                        "$.buildings[*].building_segments[*]", rmd_p
                    )
                    for swh_use in find_all(
                        "$.zones[*].spaces[*].service_water_heating_uses[*]",
                        building_segment,
                    )
                ]
            )

            return swh_use_loads_p <= 0.0

        def get_calc_vals(self, context, data=None):
            rmd_b = context.BASELINE_0
            swh_use_loads_b = sum(
                [
                    swh_use.get("use", 0.0)
                    # The json path needs to update if schema changes.
                    for building_segment in find_all(
                        "$.buildings[*].building_segments[*]", rmd_b
                    )
                    for swh_use in find_all(
                        "$.zones[*].spaces[*].service_water_heating_uses[*]",
                        building_segment,
                    )
                ]
            )
            return {"swh_use_loads_b": swh_use_loads_b}

        def rule_check(self, context, calc_vals=None, data=None):
            swh_use_loads_b = calc_vals["swh_use_loads_b"]
            return swh_use_loads_b <= 0.0
