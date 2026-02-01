from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import PROPOSED
from rct229.rulesets.ashrae9012022.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)


class PRM9012022Rule82e93(RuleDefinitionListIndexedBase):
    """Rule 42 of ASHRAE 90.1-2022 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012022Rule82e93, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            id="5-42",
            description="Each linear thermal bridge and point thermal bridge as identified in Section 5.5.5 shall be modeled using either of the following techniques:"
            "a. A separate model of the assembly within the energy simulation model. b. Adjustment of the clear-field U-factor in accordance with Section A10.2.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5 Building Envelope Modeling Requirements for the Proposed building",
            is_primary_rule=False,
            each_rule=PRM9012022Rule82e93.BuildingRule(),
            index_rmd=PROPOSED,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather", "constructions"],
                "$.ruleset_model_descriptions[*].weather": ["climate_zone"],
            },
        )

    def create_data(self, context, data=None):
        rpd_p = context.PROPOSED
        climate_zone_p = rpd_p["ruleset_model_descriptions"][0]["weather"][
            "climate_zone"
        ]
        constructions_p = rpd_p["ruleset_model_descriptions"][0]["constructions"]

        return {
            "climate_zone_p": climate_zone_p,
            "constructions_p": constructions_p,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012022Rule82e93.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={},
                each_rule=PRM9012022Rule82e93.BuildingRule.SurfaceRule(),
                index_rmd=PROPOSED,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def is_applicable(self, context, data=None):
            building_p = context.PROPOSED
            climate_zone_p = data["climate_zone_p"]
            constructions_p = data["constructions_p"]

            scc_dictionary_p = get_surface_conditioning_category_dict(
                climate_zone_p, building_p, constructions_p, PROPOSED
            )

            return scc_dictionary_p

        def create_data(self, context, data):
            building_p = context.PROPOSED
            climate_zone_p = data["climate_zone_p"]
            constructions_p = data["constructions_p"]

            scc_dictionary_p = get_surface_conditioning_category_dict(
                climate_zone_p, building_p, constructions_p, PROPOSED
            )

            return {"scc_dictionary_p": scc_dictionary_p}

        class SurfaceRule(PartialRuleDefinition):
            def __init__(self):
                super(PRM9012022Rule82e93.BuildingRule.SurfaceRule, self,).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=False, PROPOSED=True
                    ),
                )

            def get_calc_vals(self, context, data=None):
                surface_p = context.PROPOSED
                scc_dictionary_p = data["scc_dictionary_p"]
                surface_con_category_p = scc_dictionary_p[surface_p["id"]]

                return {"surface_con_category_p": surface_con_category_p}

            def applicability_check(self, context, calc_vals, data):
                surface_con_category_p = calc_vals["surface_con_category_p"]

                return surface_con_category_p != SCC.UNREGULATED
