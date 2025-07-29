from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_skylight_roof_areas_dict import (
    get_building_segment_skylight_roof_areas_dict,
)
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal

SKYLIGHT_THRESHOLD = 0.03


class PRM9012019Rule78j13(RuleDefinitionListIndexedBase):
    """Rule 24 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule78j13, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule78j13.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-24",
            description="If skylight area in the proposed design is 3% or less of the roof surface, the skylight area in baseline shall be equal to that in the proposed design.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building",
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
            super(PRM9012019Rule78j13.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule78j13.BuildingRule.BuildingSegmentRule(),
                index_rmd=BASELINE_0,
                list_path="building_segments[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            building_p = context.PROPOSED
            return {
                "skylight_roof_areas_dictionary_b": get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], data["constructions"], building_b
                ),
                "skylight_roof_areas_dictionary_p": get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], data["constructions"], building_p
                ),
            }

        class BuildingSegmentRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule78j13.BuildingRule.BuildingSegmentRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    precision={
                        "skylight_roof_ratio_b": {
                            "precision": 0.01,
                            "unit": "",
                        }
                    },
                )

            def is_applicable(self, context, data=None):
                building_segment_p = context.PROPOSED
                skylight_roof_areas_dictionary_p = data[
                    "skylight_roof_areas_dictionary_p"
                ]

                total_skylight_area_p = skylight_roof_areas_dictionary_p[
                    building_segment_p["id"]
                ]["total_skylight_area"]
                total_envelope_roof_area_p = skylight_roof_areas_dictionary_p[
                    building_segment_p["id"]
                ]["total_envelope_roof_area"]
                # avoid zero division
                return (
                    total_envelope_roof_area_p > ZERO.AREA
                    and 0
                    < total_skylight_area_p / total_envelope_roof_area_p
                    <= SKYLIGHT_THRESHOLD
                )

            def get_calc_vals(self, context, data=None):
                building_segment_b = context.BASELINE_0
                skylight_roof_areas_dictionary_b = data[
                    "skylight_roof_areas_dictionary_b"
                ]
                skylight_roof_areas_dictionary_p = data[
                    "skylight_roof_areas_dictionary_p"
                ]

                return {
                    "skylight_roof_ratio_b": skylight_roof_areas_dictionary_b[
                        building_segment_b["id"]
                    ]["total_skylight_area"]
                    / skylight_roof_areas_dictionary_b[building_segment_b["id"]][
                        "total_envelope_roof_area"
                    ],
                    "skylight_total_roof_ratio_p": sum(
                        component["total_skylight_area"]
                        for component in skylight_roof_areas_dictionary_p.values()
                    )
                    / sum(
                        component["total_envelope_roof_area"]
                        for component in skylight_roof_areas_dictionary_p.values()
                    ),
                }

            def rule_check(self, context, calc_vals=None, data=None):
                return self.precision_comparison["skylight_roof_ratio_b"](
                    calc_vals["skylight_roof_ratio_b"].magnitude,
                    calc_vals["skylight_total_roof_ratio_p"].magnitude,
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                return std_equal(
                    calc_vals["skylight_roof_ratio_b"].magnitude,
                    calc_vals["skylight_total_roof_ratio_p"].magnitude,
                )
