from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.utils.jsonpath_utils import find_all


class Section11Rule15(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule15, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule15.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-15",
            description=(
                "Service water loads and use shall be the same for both the proposed design and baseline building design.Exceptions:(1) Energy Efficiency Measures approved by the Authority Having Jurisdiction are used in the proposed model (2) SWH energy consumption can be demonstrated to be reduced by reducing the required temperature of service mixed water, by increasing the temperature, or by increasing the temperature of the entering makeup water."
            ),
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, (g)",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionBase):
        def __init__(self):
            super(Section11Rule15.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            swh_use_ids = []

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_b
            ):
                service_water_heating_use_ids = (
                    get_swh_uses_associated_with_each_building_segment(
                        rmd_b, building_segment["id"]
                    )
                )
                swh_use_ids.append(service_water_heating_use_ids)

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_p
            ):
                service_water_heating_use_ids = (
                    get_swh_uses_associated_with_each_building_segment(
                        rmd_p, building_segment["id"]
                    )
                )
                swh_use_ids.append(service_water_heating_use_ids)

            return len(swh_use_ids) > 0

        def get_calc_vals(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            swh_use_ids_b = []
            swh_use_ids_p = []

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_b
            ):
                service_water_heating_use_ids = (
                    get_swh_uses_associated_with_each_building_segment(
                        rmd_b, building_segment["id"]
                    )
                )
                swh_use_ids_b.append(service_water_heating_use_ids)

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_p
            ):
                service_water_heating_use_ids = (
                    get_swh_uses_associated_with_each_building_segment(
                        rmd_p, building_segment["id"]
                    )
                )
                swh_use_ids_p.append(service_water_heating_use_ids)

            return {"swh_use_ids_b": swh_use_ids_b, "swh_use_ids_p": swh_use_ids_p}

        def rule_check(self, context, calc_vals=None, data=None):
            return
