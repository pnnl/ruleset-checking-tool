from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.std_comparisons import std_equal

AIR_ECONOMIZER = schema_enums["AirEconomizerOptions"]
CLIMATE_ZONE_70F = ["CZ5A", "CZ6A"]
CLIMATE_ZONE_75F = [
    "CZ2B",
    "CZ3B",
    "CZ3C",
    "CZ4B",
    "CZ4C",
    "CZ5B",
    "CZ5C",
    "CZ6B",
    "CZ7",
    "CZ8",
]


class Section19Rule12(RuleDefinitionListIndexedBase):
    """Rule 12 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule12, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section19Rule12.HVACRule(),
            index_rmr="baseline",
            id="19-12",
            description="The baseline system economizer high-limit shutoff shall be a dry-bulb fixed switch with set-point temperatures in accordance with the values in Table G3.1.2.7.",
            ruleset_section_title="HVAC - General",
            standard_section=" Section G3.1.2.7",
            is_primary_rule=True,
            list_path="$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule12.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["fan_system"],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.baseline
            climate_zone_b = data["climate_zone"]
            fan_system_b = hvac_b["fan_system"]

            air_economizer_b = fan_system_b.get("air_economizer")

            return air_economizer_b is not None and (
                climate_zone_b in CLIMATE_ZONE_70F or climate_zone_b in CLIMATE_ZONE_75F
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            climate_zone_b = data["climate_zone"]
            fan_system_b = hvac_b["fan_system"]

            high_limit_temp_b = getattr_(
                fan_system_b,
                "high_limit_shutoff_temperature",
                "air_economizer",
                "high_limit_shutoff_temperature",
            )

            air_economizer_type_b = getattr_(
                fan_system_b,
                "air economizer type",
                "air_economizer",
                "type",
            )

            if climate_zone_b in CLIMATE_ZONE_70F:
                req_high_limit_temp = 70 * ureg("degR")
            elif climate_zone_b in CLIMATE_ZONE_75F:
                req_high_limit_temp = 75 * ureg("degR")

            return {
                "high_limit_temp_b": high_limit_temp_b,
                "req_high_limit_temp": req_high_limit_temp,
                "air_economizer_type_b": air_economizer_type_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            req_high_limit_temp = calc_vals["req_high_limit_temp"]
            high_limit_temp_b = calc_vals["high_limit_temp_b"]
            air_economizer_type_b = calc_vals["air_economizer_type_b"]

            return (
                std_equal(req_high_limit_temp, high_limit_temp_b)
                and air_economizer_type_b == AIR_ECONOMIZER.TEMPERATURE
            )
