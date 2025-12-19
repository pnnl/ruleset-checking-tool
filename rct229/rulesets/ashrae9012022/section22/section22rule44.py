from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import PROPOSED
from rct229.rulesets.ashrae9012022.ruleset_functions.does_chiller_performance_match_curve import (
    J4_CURVE,
    does_chiller_performance_match_curve,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

CHILLER_COMPRESSOR = SchemaEnums.schema_enums["ChillerCompressorOptions"]
UNDETERMINED_MSG = "FAIL unless manufacturer full- and part-load data is provided to support the modeled curves."


class PRM9012022Rule43f22(RuleDefinitionListIndexedBase):
    """Rule 44 of ASHRAE 90.1-2022 Appendix G Section 22 (Chilled Water Loop)"""

    def __init__(self):
        super(PRM9012022Rule43f22, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012022Rule43f22.ChillerRule(),
            index_rmd=PROPOSED,
            id="22-44",
            description="here part-load performance of chillers in the proposed design is not available, and the design temperature across the condenser is 10°F, "
            "the performance curves in Normative Appendix J, as referenced in Table J-1, shall be modeled for the specified chiller.",
            ruleset_section_title="HVAC - Chiller",
            standard_section=" Table G3.1 #10b Proposed Column",
            is_primary_rule=True,
            list_path="$.chillers[*]",
            rmd_context="ruleset_model_descriptions/0",
        )

    def create_data(self, context, data):
        rmd_p = context.PROPOSED

        return {
            "non_process_chw_coil_loop_dict_p": {
                chw_loop["id"]: [
                    chw_child_loop_id
                    for chw_child_loop_id in find_all(
                        f'$.child_loops[*][?(@.type="COOLING")].id', chw_loop
                    )
                ]
                for chw_loop in find_all(
                    f'$.fluid_loops[*][?(@.type="COOLING")]', rmd_p
                )
            }
        }

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012022Rule43f22.ChillerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={
                    "$": ["cooling_loop"],
                },
                manual_check_required_msg=UNDETERMINED_MSG,
            )

        def is_applicable(self, context, data=None):
            chiller_p = context.PROPOSED
            cooling_loop_p = chiller_p["cooling_loop"]
            non_process_chw_coil_loop_dict_p = data["non_process_chw_coil_loop_dict_p"]

            return (
                # Check if chiller primary loop serves hvac systems
                cooling_loop_p in non_process_chw_coil_loop_dict_p
                # Check if chiller serves a loop that has child loops and those child loops serve hvac systems
                or cooling_loop_p in non_process_chw_coil_loop_dict_p[cooling_loop_p]
            )

        def get_calc_vals(self, context, data=None):
            chiller_p = context.PROPOSED

            rated_capacity_p = getattr_(chiller_p, "chillers", "rated_capacity")
            compressor_type_p = getattr_(chiller_p, "chillers", "compressor_type")

            if chiller_p.get("condensing_loop") is None:
                if rated_capacity_p < 150 * ureg("ton"):
                    curve_set_list_p = [J4_CURVE.A, J4_CURVE.K]
                else:
                    curve_set_list_p = [J4_CURVE.B, J4_CURVE.L]

            else:
                if compressor_type_p in (
                    CHILLER_COMPRESSOR.POSITIVE_DISPLACEMENT,
                    CHILLER_COMPRESSOR.SCROLL,
                    CHILLER_COMPRESSOR.SCREW,
                ):
                    if rated_capacity_p < 75 * ureg("ton"):
                        curve_set_list_p = [J4_CURVE.C, J4_CURVE.M]
                    elif rated_capacity_p < 150 * ureg("ton"):
                        curve_set_list_p = [J4_CURVE.D, J4_CURVE.N]
                    elif rated_capacity_p < 300 * ureg("ton"):
                        curve_set_list_p = [J4_CURVE.E, J4_CURVE.O]
                    elif rated_capacity_p < 600 * ureg("ton"):
                        curve_set_list_p = [J4_CURVE.F, J4_CURVE.P]
                    else:
                        curve_set_list_p = [J4_CURVE.G, J4_CURVE.Q]

                if compressor_type_p == CHILLER_COMPRESSOR.CENTRIFUGAL:
                    if rated_capacity_p < 150 * ureg("ton"):
                        curve_set_list_p = [J4_CURVE.H, J4_CURVE.R]
                    elif rated_capacity_p < 300 * ureg("ton"):
                        curve_set_list_p = [J4_CURVE.H, J4_CURVE.S]
                    elif rated_capacity_p < 400 * ureg("ton"):
                        curve_set_list_p = [J4_CURVE.I, J4_CURVE.T]
                    else:
                        curve_set_list_p = [J4_CURVE.J, J4_CURVE.U]

            design_leaving_condenser_temperature_p = getattr_(
                chiller_p, "chillers", "design_leaving_condenser_temperature"
            )
            design_entering_condenser_temperature_p = getattr_(
                chiller_p, "chillers", "design_entering_condenser_temperature"
            )

            return {
                "curve_set_list_p": curve_set_list_p,
                "design_leaving_condenser_temperature_p": CalcQ(
                    "temperature", design_leaving_condenser_temperature_p
                ),
                "design_entering_condenser_temperature_p": CalcQ(
                    "temperature", design_entering_condenser_temperature_p
                ),
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            chiller_p = context.PROPOSED
            curve_set_list_p = calc_vals["curve_set_list_p"]

            return not any(
                does_chiller_performance_match_curve(chiller_p, curve_set)
                for curve_set in curve_set_list_p
            )

        def rule_check(self, context, calc_vals=None, data=None):
            chiller_p = context.PROPOSED
            curve_set_list_p = calc_vals["curve_set_list_p"]
            design_leaving_condenser_temperature_p = calc_vals[
                "design_leaving_condenser_temperature_p"
            ]
            design_entering_condenser_temperature_p = calc_vals[
                "design_entering_condenser_temperature_p"
            ]

            return any(
                does_chiller_performance_match_curve(chiller_p, curve_set)
                for curve_set in curve_set_list_p
            ) and std_equal(
                design_entering_condenser_temperature_p
                - design_leaving_condenser_temperature_p,
                10 * ureg("delta_degF"),
            )
