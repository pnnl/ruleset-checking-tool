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


class PRM9012019Rule84u02(RuleDefinitionListIndexedBase):
    """Rule 25 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule84u02, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "$.ruleset_model_descriptions[*].weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule84u02.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-25",
            description="If the skylight area of the proposed design is greater than 3%, baseline skylight area shall be decreased in all roof components in which skylights are located to reach 3%.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={
                "climate_zone": (
                    BASELINE_0,
                    "ruleset_model_descriptions[0]/weather/climate_zone",
                )
            },
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions = rpd_b["ruleset_model_descriptions"][0].get("constructions")
        return {"climate_zone": climate_zone, "constructions": constructions}

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule84u02.BuildingRule, self).__init__(
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
            building_p = context.PROPOSED
            skylight_roof_areas_p = get_building_segment_skylight_roof_areas_dict(
                data["climate_zone"], data["constructions"], building_p
            )
            total_skylight_area = sum(
                v["total_skylight_area"] for v in skylight_roof_areas_p.values()
            )
            total_roof_area = sum(
                v["total_envelope_roof_area"] for v in skylight_roof_areas_p.values()
            )

            return (
                total_roof_area > ZERO.AREA
                and total_skylight_area / total_roof_area > SKYLIGHT_THRESHOLD
            )

        def get_calc_vals(self, context, data=None):
            building_b = context.BASELINE_0
            building_p = context.PROPOSED

            skylight_roof_areas_dictionary_b = (
                get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], data["constructions"], building_b
                )
            )
            skylight_roof_areas_dictionary_p = (
                get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], data["constructions"], building_p
                )
            )
            total_skylight_area_b = sum(
                v["total_skylight_area"]
                for v in skylight_roof_areas_dictionary_b.values()
            )
            total_roof_area_b = sum(
                v["total_envelope_roof_area"]
                for v in skylight_roof_areas_dictionary_b.values()
            )

            total_skylight_area_p = sum(
                v["total_skylight_area"]
                for v in skylight_roof_areas_dictionary_p.values()
            )
            total_roof_area_p = sum(
                v["total_envelope_roof_area"]
                for v in skylight_roof_areas_dictionary_p.values()
            )
            skylight_roof_ratio_b = total_skylight_area_b / total_roof_area_b
            skylight_roof_ratio_p = total_skylight_area_p / total_roof_area_p

            return {
                "total_skylight_area_b": total_skylight_area_b,
                "total_roof_area_b": total_roof_area_b,
                "total_skylight_area_p": total_skylight_area_p,
                "total_roof_area_p": total_roof_area_p,
                "skylight_roof_ratio_b": skylight_roof_ratio_b,
                "skylight_roof_ratio_p": skylight_roof_ratio_p,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return self.precision_comparison["skylight_roof_ratio_b"](
                calc_vals["skylight_roof_ratio_b"].magnitude, SKYLIGHT_THRESHOLD
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            skylight_roof_ratio_b = calc_vals["skylight_roof_ratio_b"]
            return std_equal(SKYLIGHT_THRESHOLD, skylight_roof_ratio_b)
