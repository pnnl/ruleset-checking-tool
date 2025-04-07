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
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="19-3",
            description="Weather conditions used in sizing runs to determine baseline equipment capacities shall be based either on design days developed using 99.6% heating design temperatures "
            "and 1% dry-bulb and 1% wet-bulb cooling design temperatures.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2.1",
            is_primary_rule=False,
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
            },
        )

    def get_calc_vals(self, context, data=None):
        rpd_b = context.BASELINE_0
        weather_b = rpd_b["ruleset_model_descriptions"][0]["weather"]
        return {
            "cooling_design_day_type": weather_b.get("cooling_design_day_type"),
            "heating_design_day_type": weather_b.get("heating_design_day_type"),
        }

    def applicability_check(self, context, calc_vals, data):
        cooling_design_day_type = calc_vals["cooling_design_day_type"]
        heating_design_day_type = calc_vals["heating_design_day_type"]

        return (cooling_design_day_type is None or heating_design_day_type is None) or (
            cooling_design_day_type == COOLING_DESIGN_DAY.COOLING_1_0
            and heating_design_day_type == HEATING_DESIGN_DAY.HEATING_99_6
        )

    def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
        cooling_design_day_type = calc_vals["cooling_design_day_type"]
        heating_design_day_type = calc_vals["heating_design_day_type"]

        if cooling_design_day_type is None or heating_design_day_type is None:
            undetermined_msg = (
                "The Heating & Cooling Design Day types were not defined. Check that the weather conditions used in sizing runs to determine baseline equipment capacities is based on design days developed using 99.6% heating design temperatures "
                "and 1% dry-bulb and 1% wet-bulb cooling design temperatures."
            )
        else:
            undetermined_msg = (
                "Check that the weather conditions used in sizing runs to determine baseline equipment capacities is based on design days developed using 99.6% heating design temperatures "
                "and 1% dry-bulb and 1% wet-bulb cooling design temperatures."
            )

        return undetermined_msg
