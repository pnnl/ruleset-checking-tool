from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
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

ABSORPTION_THERMAL_EXTERIOR = 0.9
UNDETERMINED_MSG = (
    "Roof surface emittance in the proposed model {absorptance_thermal_exterior} matches that in the "
    "user model but is not equal to the prescribed default value of 0.9. Verify that the modeled value "
    "is based on testing in accordance with section 5.5.3.1.1(a). "
)
PASS_DIFFERS_MSG = (
    "Roof thermal emittance is equal to the prescribed default value of 0.9 but differs from the "
    "thermal emittance in the user model {absorptance_thermal_exterior} "
)


class Section5Rule30(RuleDefinitionListIndexedBase):
    """Rule 30 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule30, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=Section5Rule30.BuildingRule(),
            index_rmr=PROPOSED,
            id="5-30",
            description="The proposed roof surfaces shall be modeled using the same thermal emittance as in the user model.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": (PROPOSED, "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule30.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=True, BASELINE_0=False, PROPOSED=True
                ),
                each_rule=Section5Rule30.BuildingRule.RoofRule(),
                index_rmr=PROPOSED,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_p = context.PROPOSED
            return {
                "scc_dict_p": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_p
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
                super(Section5Rule30.BuildingRule.RoofRule, self).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=True, BASELINE_0=False, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["optical_properties"],
                        "optical_properties": ["absorptance_thermal_exterior"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                roof_p = context.PROPOSED
                roof_u = context.USER

                return {
                    "absorptance_thermal_exterior_p": roof_p["optical_properties"][
                        "absorptance_thermal_exterior"
                    ],
                    "absorptance_thermal_exterior_u": roof_u["optical_properties"][
                        "absorptance_thermal_exterior"
                    ],
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                absorptance_thermal_exterior_p = calc_vals[
                    "absorptance_thermal_exterior_p"
                ]
                absorptance_thermal_exterior_u = calc_vals[
                    "absorptance_thermal_exterior_u"
                ]
                return (
                    absorptance_thermal_exterior_p == absorptance_thermal_exterior_u
                    and absorptance_thermal_exterior_p != ABSORPTION_THERMAL_EXTERIOR
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                absorptance_thermal_exterior_p = calc_vals[
                    "absorptance_thermal_exterior_p"
                ]
                return UNDETERMINED_MSG.format(
                    absorptance_thermal_exterior=absorptance_thermal_exterior_p
                )

            def rule_check(self, context, calc_vals=None, data=None):
                return (
                    calc_vals["absorptance_thermal_exterior_p"]
                    == ABSORPTION_THERMAL_EXTERIOR
                )

            def get_pass_msg(self, context, calc_vals=None, data=None):
                """Pre-condition: see rule_check"""
                absorptance_thermal_exterior_p = calc_vals[
                    "absorptance_thermal_exterior_p"
                ]
                absorptance_thermal_exterior_u = calc_vals[
                    "absorptance_thermal_exterior_u"
                ]

                pass_msg = (
                    PASS_DIFFERS_MSG.format(
                        absorptance_thermal_exterior=absorptance_thermal_exterior_u
                    )
                    if absorptance_thermal_exterior_p != absorptance_thermal_exterior_u
                    else ""
                )

                return pass_msg
