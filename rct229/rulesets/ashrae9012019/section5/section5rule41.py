from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
    OpaqueSurfaceType as OST,
)

ABSORPTION_THERMAL_EXTERIOR = 0.9
UNDETERMINED_MSG = "Roof surface emittance in the proposed model {absorptance_thermal_exterior} matches that in the " \
                   "user model but is not equal to the prescribed default value of 0.9. Verify that the modeled value " \
                   "is based on testing in accordance with section 5.5.3.1.1(a). "
PASS_DIFFERS_MSG = "Roof thermal emittance is equal to the prescribed default value of 0.9 but differs from the " \
                   "thermal emittance in the user model {absorptance_thermal_exterior} "


class Section5Rule41(RuleDefinitionListIndexedBase):
    """Rule 41 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule41, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section5Rule41.BuildingRule(),
            index_rmr="proposed",
            id="5-41",
            description="The proposed roof surfaces shall be modeled using the same thermal emittance as in the user model.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule41.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, True),
                each_rule=Section5Rule41.BuildingRule.RoofRule(),
                index_rmr="baseline",
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def list_filter(self, context_item, data=None):
            surface_p = context_item.proposed
            return get_opaque_surface_type(surface_p) == OST.ROOF

        class RoofRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule41.BuildingRule.RoofRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(True, False, True),
                    required_fields={
                        "$": ["surface_optical_properties"],
                        "surface_optical_properties": ["absorptance_thermal_exterior"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                roof_p = context.proposed
                roof_u = context.user

                return {
                    "absorptance_thermal_exterior_p": roof_p[
                        "surface_optical_properties"
                    ]["absorptance_thermal_exterior"],
                    "absorptance_thermal_exterior_u": roof_u[
                        "surface_optical_properties"
                    ]["absorptance_thermal_exterior"],
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
