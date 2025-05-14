from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.schema.schema_enums import SchemaEnums

HEATING_DESIGN_DAY = SchemaEnums.schema_enums["HeatingDesignDayOptions"]
COOLING_DESIGN_DAY = SchemaEnums.schema_enums["CoolingDesignDayOptions"]


class PRM9012019Rule16j07(PartialRuleDefinition):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule16j07, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            id="19-3",
            description="Weather conditions used in sizing runs to determine baseline equipment capacities shall be based either on design days developed "
            "using 99.6% heating design temperatures and 1% dry-bulb and 1% wet-bulb cooling design temperatures.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2.1",
            is_primary_rule=True,
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
            },
        )

    def get_calc_vals(self, context, data=None):
        rpd_b = context.BASELINE_0
        rpd_p = context.PROPOSED

        weather_b = rpd_b["ruleset_model_descriptions"][0]["weather"]
        weather_p = rpd_p["ruleset_model_descriptions"][0]["weather"]

        return {
            "cooling_design_day_type_b": weather_b.get(
                "cooling_dry_bulb_design_day_type"
            ),
            "heating_design_day_type_b": weather_b.get(
                "heating_dry_bulb_design_day_type"
            ),
            "evaporation_wet_bulb_design_day_type_b": weather_b.get(
                "evaporation_wet_bulb_design_day_type"
            ),
            "cooling_design_day_type_p": weather_p.get(
                "cooling_dry_bulb_design_day_type"
            ),
            "heating_design_day_type_p": weather_p.get(
                "heating_dry_bulb_design_day_type"
            ),
            "evaporation_wet_bulb_design_day_type_p": weather_p.get(
                "evaporation_wet_bulb_design_day_type"
            ),
        }

    def rule_check(self, context, calc_vals=None, data={}):
        cooling_design_day_type_b = calc_vals["cooling_design_day_type_b"]
        heating_design_day_type_b = calc_vals["heating_design_day_type_b"]
        evaporation_wet_bulb_design_day_type_b = calc_vals[
            "evaporation_wet_bulb_design_day_type_b"
        ]
        cooling_design_day_type_p = calc_vals["cooling_design_day_type_p"]
        heating_design_day_type_p = calc_vals["heating_design_day_type_p"]
        evaporation_wet_bulb_design_day_type_p = calc_vals[
            "evaporation_wet_bulb_design_day_type_p"
        ]

        return (
            cooling_design_day_type_b
            == evaporation_wet_bulb_design_day_type_b
            == COOLING_DESIGN_DAY.COOLING_1_0
            and heating_design_day_type_b == HEATING_DESIGN_DAY.HEATING_99_6
        ) and (
            cooling_design_day_type_p
            == evaporation_wet_bulb_design_day_type_p
            == COOLING_DESIGN_DAY.COOLING_1_0
            and heating_design_day_type_p == HEATING_DESIGN_DAY.HEATING_99_6
        )

    def get_fail_msg(self, context, calc_vals=None, data=None):
        cooling_design_day_type_p = calc_vals["cooling_design_day_type_p"]
        heating_design_day_type_p = calc_vals["heating_design_day_type_p"]
        evaporation_wet_bulb_design_day_type_p = calc_vals[
            "evaporation_wet_bulb_design_day_type_p"
        ]

        if not (
            cooling_design_day_type_p
            == evaporation_wet_bulb_design_day_type_p
            == COOLING_DESIGN_DAY.COOLING_1_0
            and heating_design_day_type_p == HEATING_DESIGN_DAY.HEATING_99_6
        ):
            FAIL_MSG = "Fail unless there are no yet to be designed HVAC systems in the proposed design."
        else:
            FAIL_MSG = ""

        return FAIL_MSG
