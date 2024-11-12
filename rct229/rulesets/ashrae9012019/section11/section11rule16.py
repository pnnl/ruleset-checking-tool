from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums

ENERGY_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]

MANUAL_CHECK_REQUIRED_MSG = (
    "The baseline service water heating has propane as a fuel source. "
    "Natural gas is the required fuel source for the baseline model except in cases where natural gas is not available on-site. "
    "Verify that natural gas is not available for the proposed building site as determined by the rating authority."
)


class Section11Rule16(RuleDefinitionListIndexedBase):
    """Rule 16 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule16, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule16.SWHEquipRule(),
            index_rmd=BASELINE_0,
            id="11-16",
            description="Gas water heaters shall be modeled using natural gas as their fuel. Exceptions: Where natural gas is not available for the proposed building site, as determined by the rating authority, gas water heaters shall be modeled using propane as their fuel.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, (h)",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].service_water_heating_equipment[*]",
        )

    class SWHEquipRule(RuleDefinitionBase):
        def __init__(self):
            super(Section11Rule16.SWHEquipRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=True,
                ),
                required_fields={
                    "$": ["heater_fuel_type"],
                },
                manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
            )

        def is_applicable(self, context, data=None):
            swh_equip_b = context.BASELINE_0
            heater_fuel_type_b = swh_equip_b["heater_fuel_type"]

            return heater_fuel_type_b != ENERGY_SOURCE.ELECTRICITY

        def manual_check_required(self, context, calc_vals=None, data=None):
            swh_equip_b = context.BASELINE_0
            swh_equip_p = context.PROPOSED

            heater_fuel_type_b = swh_equip_b["heater_fuel_type"]
            heater_fuel_type_p = swh_equip_p["heater_fuel_type"]

            return (
                heater_fuel_type_b == ENERGY_SOURCE.PROPANE
                and heater_fuel_type_p != ENERGY_SOURCE.NATURAL_GAS
            )

        def get_calc_vals(self, context, data=None):
            swh_equip_b = context.BASELINE_0
            swh_equip_P = context.PROPOSED

            heater_fuel_type_b = swh_equip_b["heater_fuel_type"]
            heater_fuel_type_p = swh_equip_P["heater_fuel_type"]

            return {
                "heater_fuel_type_b": heater_fuel_type_b,
                "heater_fuel_type_p": heater_fuel_type_p,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            heater_fuel_type_b = calc_vals["heater_fuel_type_b"]

            return heater_fuel_type_b == ENERGY_SOURCE.NATURAL_GAS

        def get_fail_msg(self, context, calc_vals=None, data=None):
            heater_fuel_type_b = calc_vals["heater_fuel_type_b"]
            heater_fuel_type_p = calc_vals["heater_fuel_type_p"]

            return (
                heater_fuel_type_b == ENERGY_SOURCE.PROPANE
                and heater_fuel_type_p == ENERGY_SOURCE.NATURAL_GAS
            )
