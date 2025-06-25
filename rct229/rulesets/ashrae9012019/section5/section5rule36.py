from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal


class PRM9012019Rule23m90(RuleDefinitionListIndexedBase):
    """Rule 36 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule23m90, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule23m90.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-36",
            description="The air leakage rate in unconditioned and unenclosed spaces must be the same the baseline and proposed design.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-1 Building Envelope Modeling Requirements for the Proposed design and Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions = rpd_b["ruleset_model_descriptions"][0].get("constructions")
        return {
            "climate_zone": climate_zone,
            "constructions": constructions,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule23m90.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule23m90.BuildingRule.ZoneRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            return {
                "zcc_dict_b": get_zone_conditioning_category_dict(
                    data["climate_zone"], building_b, data["constructions"]
                ),
            }

        def list_filter(self, context_item, data=None):
            zcc_dict_b = data["zcc_dict_b"]
            zone_b = context_item.BASELINE_0
            return zcc_dict_b[zone_b["id"]] in [ZCC.UNCONDITIONED, ZCC.UNENCLOSED]

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule23m90.BuildingRule.ZoneRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["infiltration"],
                        "infiltration": ["flow_rate"],
                    },
                    precision={
                        "total_infiltration_rate_b": {
                            "precision": 0.1,
                            "unit": "cfm",
                        }
                    },
                )

            def get_calc_vals(self, context, data=None):
                zone_b = context.BASELINE_0
                zone_p = context.PROPOSED

                zone_infiltration_flow_rate_b = zone_b["infiltration"]["flow_rate"]
                zone_infiltration_flow_rate_p = zone_p["infiltration"]["flow_rate"]

                return {
                    "baseline_infiltration": CalcQ(
                        "air_flow_rate", zone_infiltration_flow_rate_b
                    ),
                    "proposed_infiltration": CalcQ(
                        "air_flow_rate", zone_infiltration_flow_rate_p
                    ),
                }

            def rule_check(self, context, calc_vals=None, data=None):
                return self.precision_comparison["total_infiltration_rate_b"](
                    calc_vals["baseline_infiltration"],
                    calc_vals["proposed_infiltration"],
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                return std_equal(
                    calc_vals["baseline_infiltration"],
                    calc_vals["proposed_infiltration"],
                )
