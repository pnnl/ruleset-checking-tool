from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.std_comparisons import std_equal

ABSORPTANCE_SOLAR_EXTERIOR = 0.7

CASE2_UNDETERMINED_MSG = (
    "Roof surface solar reflectance in the proposed model {absorptance_solar_exterior} matches that in the user model but is not equal to the prescribed default value of 0.3. "
    "Verify that reflectance was established using aged test data as required in section 5.5.3.1(a)."
)
CASE3_UNDETERMINED_MSG = (
    "Fail if the thermal emittance in the user model is based on aged test data. roof surface solar reflectance is equal to the prescribed default value of 0.3 "
    "but differs from the solar reflectance in the user model 1-{absorptance_solar_exterior}."
)
PASS_DIFFERS_MSG_REGULATED = "Roof surface solar reflectance is equal to the prescribed default value of 0.3 but differs from the solar reflectance in the user model {absorptance_solar_exterior}"


class PRM9012019Rule78r30(RuleDefinitionListIndexedBase):
    """Rule 32 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule78r30, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule78r30.BuildingRule(),
            index_rmd=PROPOSED,
            id="5-32",
            description="The proposed roof surfaces shall be modeled using the same solar reflectance as in the user "
            "model if the aged test data are available, or equal to 0.7 default reflectance",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_p = context.PROPOSED
        climate_zone = rpd_p["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions = rpd_p["ruleset_model_descriptions"][0].get("constructions")
        return {
            "climate_zone": climate_zone,
            "constructions": constructions,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule78r30.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True, BASELINE_0=False, PROPOSED=True
                ),
                each_rule=PRM9012019Rule78r30.BuildingRule.RoofRule(),
                index_rmd=PROPOSED,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_p = context.PROPOSED
            return {
                "scc_dict_p": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_p, data["constructions"]
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_p = context_item.PROPOSED
            scc = data["scc_dict_p"][surface_p["id"]]
            return (
                get_opaque_surface_type(surface_p) == OST.ROOF
                and scc is not SCC.UNREGULATED
            )

        class RoofRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule78r30.BuildingRule.RoofRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=True, BASELINE_0=False, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["optical_properties"],
                        "optical_properties": ["absorptance_solar_exterior"],
                    },
                    precision={
                        "absorptance_solar_exterior_p": {
                            "precision": 0.01,
                            "unit": "",
                        }
                    },
                )

            def get_calc_vals(self, context, data=None):
                roof_p = context.PROPOSED
                roof_u = context.USER
                scc_dict_p = data["scc_dict_p"]

                return {
                    "absorptance_solar_exterior_p": roof_p["optical_properties"][
                        "absorptance_solar_exterior"
                    ],
                    "absorptance_solar_exterior_u": roof_u["optical_properties"][
                        "absorptance_solar_exterior"
                    ],
                    "surface_conditioning_category_p": scc_dict_p[roof_p["id"]],
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                absorptance_solar_exterior_p = calc_vals["absorptance_solar_exterior_p"]
                absorptance_solar_exterior_u = calc_vals["absorptance_solar_exterior_u"]

                return (
                    absorptance_solar_exterior_p == absorptance_solar_exterior_u
                    and absorptance_solar_exterior_p != ABSORPTANCE_SOLAR_EXTERIOR
                ) or (
                    absorptance_solar_exterior_p != absorptance_solar_exterior_u
                    and self.precision_comparison["absorptance_solar_exterior_p"](
                        absorptance_solar_exterior_p,
                        ABSORPTANCE_SOLAR_EXTERIOR,
                    )
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                absorptance_solar_exterior_p = calc_vals["absorptance_solar_exterior_p"]
                absorptance_solar_exterior_u = calc_vals["absorptance_solar_exterior_u"]

                UNDETERMINED_MSG = ""
                if (
                    absorptance_solar_exterior_p == absorptance_solar_exterior_u
                    and absorptance_solar_exterior_p != ABSORPTANCE_SOLAR_EXTERIOR
                ):
                    UNDETERMINED_MSG = CASE2_UNDETERMINED_MSG.format(
                        absorptance_solar_exterior=absorptance_solar_exterior_p
                    )
                elif (
                    absorptance_solar_exterior_p != absorptance_solar_exterior_u
                    and self.precision_comparison["absorptance_solar_exterior_p"](
                        absorptance_solar_exterior_p,
                        ABSORPTANCE_SOLAR_EXTERIOR,
                    )
                ):
                    UNDETERMINED_MSG = CASE3_UNDETERMINED_MSG.format(
                        absorptance_solar_exterior=absorptance_solar_exterior_p
                    )

                return UNDETERMINED_MSG

            def rule_check(self, context, calc_vals=None, data=None):
                return self.precision_comparison["absorptance_solar_exterior_p"](
                    calc_vals["absorptance_solar_exterior_p"],
                    ABSORPTANCE_SOLAR_EXTERIOR,
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                return std_equal(
                    calc_vals["absorptance_solar_exterior_p"],
                    ABSORPTANCE_SOLAR_EXTERIOR,
                )

            def get_pass_msg(self, context, calc_vals=None, data=None):
                """Pre-condition: see rule_check"""
                absorptance_solar_exterior_p = calc_vals["absorptance_solar_exterior_p"]
                absorptance_solar_exterior_u = calc_vals["absorptance_solar_exterior_u"]

                # this condition only applies when P-RMD = 0.7 and P-RMD surface is regulated.
                PASS_MSG = (
                    PASS_DIFFERS_MSG_REGULATED.format(
                        absorptance_solar_exterior=(1 - absorptance_solar_exterior_u)
                    )
                    if absorptance_solar_exterior_p != absorptance_solar_exterior_u
                    else ""
                )
                return PASS_MSG
