from collections import deque

from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.utils.jsonpath_utils import find_all


class PRM9012019Rule29n09(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule29n09, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule29n09.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-6",
            description="Piping losses shall not be modeled.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, i",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule29n09.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule29n09.RMDRule.SWHDistRule(),
                index_rmd=BASELINE_0,
                list_path="$.service_water_heating_distribution_systems[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0

            swh_dist_sys_list_b = find_all(
                "$.service_water_heating_distribution_systems[*]", rmd_b
            )

            return swh_dist_sys_list_b

        class SWHDistRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule29n09.RMDRule.SWHDistRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=True,
                        PROPOSED=False,
                    ),
                    required_fields={
                        "$": ["service_water_piping"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                swh_dist_sys_b = context.BASELINE_0

                piping_losses_modeled_b = []
                piping = swh_dist_sys_b.get("service_water_piping")
                if piping:
                    queue = deque([piping])
                    while queue:
                        current_piping = queue.popleft()
                        children_piping = current_piping.get("child", [])
                        queue.extend(children_piping)

                        piping_losses_modeled_b.append(
                            current_piping.get("are_thermal_losses_modeled")
                        )

                return {"piping_losses_modeled_b": piping_losses_modeled_b}

            def rule_check(self, context, calc_vals=None, data=None):
                piping_losses_modeled_b = calc_vals["piping_losses_modeled_b"]

                return not any(piping_losses_modeled_b)
