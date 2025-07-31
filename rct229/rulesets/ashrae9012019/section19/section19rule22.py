from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_

ENERGY_RECOVERY_OPERATION = SchemaEnums.schema_enums["EnergyRecoveryOperationOptions"]


class PRM9012019Rule44t17(RuleDefinitionListIndexedBase):
    """Rule 22 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule44t17, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule44t17.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-22",
            description="Baseline systems modeled with exhaust air energy recovery shall allow bypass or control heat recovery system to permit air economizer operation.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2",
            is_primary_rule=True,
            list_path="$.ruleset_model_descriptions[0].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule44t17.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            fan_sys_b = hvac_b["fan_system"]

            return fan_sys_b.get("air_energy_recovery") is not None

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            fan_sys_b = hvac_b["fan_system"]

            ER_operation = getattr_(
                fan_sys_b,
                "Fan System",
                "air_energy_recovery",
                "energy_recovery_operation",
            )
            return {"ER_operation": ER_operation}

        def rule_check(self, context, calc_vals=None, data=None):
            ER_operation = calc_vals["ER_operation"]

            return ER_operation == ENERGY_RECOVERY_OPERATION.WHEN_MINIMUM_OUTSIDE_AIR
