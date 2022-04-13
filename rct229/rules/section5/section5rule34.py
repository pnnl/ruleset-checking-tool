from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_building_segment_skylight_roof_areas_dict import (
    get_building_segment_skylight_roof_areas_dict,
)
from rct229.utils.std_comparisons import std_equal

SKYLIGHT_THRESHOLD = 0.3


class Section5Rule34(RuleDefinitionListIndexedBase):
    """Rule 34 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule34, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule34.BuildingRule(),
            index_rmr="baseline",
            id="5-15",
            description="If skylight area in the proposed design is 3% or less of the roof surface, the skylight area in baseline shall be equal to that in the proposed design.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule34.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section5Rule34.BuildingRule.BuildingSegmentRule(),
                index_rmr="baseline",
                list_path="building_segments[*]",
            )

        def create_data(self, context, data=None):
            baseline = context.baseline
            proposed = context.proposed
            # Merge into the existing data dict
            return {
                **data,
                "skylight_roof_areas_dictionary_b": get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], baseline
                ),
                "skylight_roof_areas_dictionary_p": get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], proposed
                ),
            }

        class BuildingSegmentRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule34.BuildingRule.BuildingSegmentRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                )

            def is_applicable(self, context, data=None):
                proposed = context.proposed
                skylight_roof_areas_dictionary_p = data[
                    "skylight_roof_areas_dictionary_p"
                ]
                skylight_roof_ratio_p = (
                    skylight_roof_areas_dictionary_p[proposed["id"]][
                        "total_skylight_area"
                    ]
                    / skylight_roof_areas_dictionary_p[proposed["id"]][
                        "total_envelope_roof_area"
                    ],
                )
                return skylight_roof_ratio_p <= SKYLIGHT_THRESHOLD

            def get_calc_vals(self, context, data=None):
                baseline = context.baseline
                proposed = context.proposed
                skylight_roof_areas_dictionary_b = data[
                    "skylight_roof_areas_dictionary_b"
                ]
                skylight_roof_areas_dictionary_p = data[
                    "skylight_roof_areas_dictionary_p"
                ]

                return {
                    "skylight_roof_ratio_b": skylight_roof_areas_dictionary_b[
                        baseline["id"]
                    ]["total_skylight_area"]
                    / skylight_roof_areas_dictionary_b[baseline["id"]][
                        "total_envelope_roof_area"
                    ],
                    "skylight_roof_ratio_p": skylight_roof_areas_dictionary_p[
                        proposed["id"]
                    ]["total_skylight_area"]
                    / skylight_roof_areas_dictionary_p[proposed["id"]][
                        "total_envelope_roof_area"
                    ],
                }

            def rule_check(self, context, calc_vals=None, data=None):
                skylight_roof_ratio_b = calc_vals["skylight_roof_ratio_b"]
                skylight_roof_ratio_p = calc_vals["skylight_roof_ratio_p"]
                return std_equal(skylight_roof_ratio_b, skylight_roof_ratio_p)
