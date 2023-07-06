from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
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

ABSORPTANCE_SOLAR_EXTERIOR = 0.7

UNDETERMINED_MSG = "Roof surface solar reflectance in the proposed model {absorptance_solar_exterior} matches that in the user model but is not equal to the prescribed default value of 0.3. Verify that reflectance was established using aged test data as required in section 5.5.3.1(a)."
PASS_DIFFERS_MSG_REGULATED = "Roof surface solar reflectance is equal to the prescribed default value of 0.3 but differs from the solar reflectance in the user model {absorptance_solar_exterior}"


class Section5Rule43(RuleDefinitionListIndexedBase):
    """Rule 43 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule43, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section5Rule43.BuildingRule(),
            index_rmr="proposed",
            id="5-43",
            description="The proposed roof surfaces shall be modeled using the same solar reflectance as in the user "
            "model if the aged test data are available, or equal to 0.7 default reflectance",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("proposed", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule43.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, True),
                each_rule=Section5Rule43.BuildingRule.RoofRule(),
                index_rmr="proposed",
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_p = context.proposed
            return {
                "scc_dict_p": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_p
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_p = context_item.proposed
            scc = data["scc_dict_p"][surface_p["id"]]
            return (
                get_opaque_surface_type(surface_p) == OST.ROOF
                and scc is not SCC.UNREGULATED
            )

        class RoofRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule43.BuildingRule.RoofRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(True, False, True),
                    required_fields={
                        "$": ["surface_optical_properties"],
                        "surface_optical_properties": ["absorptance_solar_exterior"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                roof_p = context.proposed
                roof_u = context.user
                scc_dict_p = data["scc_dict_p"]

                return {
                    "absorptance_solar_exterior_p": roof_p[
                        "surface_optical_properties"
                    ]["absorptance_solar_exterior"],
                    "absorptance_solar_exterior_u": roof_u[
                        "surface_optical_properties"
                    ]["absorptance_solar_exterior"],
                    "surface_conditioning_category_p": scc_dict_p[roof_p["id"]],
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                absorptance_solar_exterior_p = calc_vals["absorptance_solar_exterior_p"]
                absorptance_solar_exterior_u = calc_vals["absorptance_solar_exterior_u"]
                return (
                    absorptance_solar_exterior_p == absorptance_solar_exterior_u
                    and absorptance_solar_exterior_p != ABSORPTANCE_SOLAR_EXTERIOR
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                absorptance_solar_exterior_p = calc_vals["absorptance_solar_exterior_p"]
                return UNDETERMINED_MSG.format(
                    absorptance_solar_exterior=absorptance_solar_exterior_p
                )

            def rule_check(self, context, calc_vals=None, data=None):
                return (
                    calc_vals["absorptance_solar_exterior_p"]
                    == ABSORPTANCE_SOLAR_EXTERIOR
                )

            def get_pass_msg(self, context, calc_vals=None, data=None):
                """Pre-condition: see rule_check"""
                absorptance_solar_exterior_p = calc_vals["absorptance_solar_exterior_p"]
                absorptance_solar_exterior_u = calc_vals["absorptance_solar_exterior_u"]

                # this condition only applies when P-RMD = 0.7 and P-RMD surface is regulated.
                pass_msg = (
                    PASS_DIFFERS_MSG_REGULATED.format(
                        absorptance_solar_exterior=(1 - absorptance_solar_exterior_u)
                    )
                    if absorptance_solar_exterior_p != absorptance_solar_exterior_u
                    else ""
                )
                return pass_msg
