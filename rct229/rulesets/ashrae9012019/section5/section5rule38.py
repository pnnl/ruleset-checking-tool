from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.utils.jsonpath_utils import find_all

UNDETERMINED_MSG = "It cannot be determined if the ground temperature schedule for the project is representative of the project climate."
NOT_DEFINED_MSG = "A ground temperature schedule was not found for the project."


class PRM9012019Rule40i28(PartialRuleDefinition):
    """Rule 38 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule40i28, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="5-38",
            description="It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through below-grade walls and basement floors.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-14(b) Building Envelope Modeling Requirements for the Proposed design and Baseline",
            is_primary_rule=False,
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
            },
        )

    def get_calc_vals(self, context, data=None):
        rpd = context.BASELINE_0
        ground_temperature_schedule = rpd["ruleset_model_descriptions"][0][
            "weather"
        ].get("ground_temperature_schedule")
        return {"ground_temperature_schedule": ground_temperature_schedule}

    def applicability_check(self, context, calc_vals, data):
        rpd = context.BASELINE_0
        return any(
            [
                get_opaque_surface_type(surface_b)
                in [OST.BELOW_GRADE_WALL, OST.UNHEATED_SOG, OST.HEATED_SOG]
                for surface_b in find_all(
                    "$.ruleset_model_descriptions[0].buildings[*].building_segments[*].zones["
                    "*].surfaces[*]",
                    rpd,
                )
            ]
        )

    def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
        if calc_vals["ground_temperature_schedule"] is None:
            return NOT_DEFINED_MSG
        return UNDETERMINED_MSG
