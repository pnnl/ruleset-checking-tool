from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.std_comparisons import std_equal

AIR_ECONOMIZER = SchemaEnums.schema_enums["AirEconomizerOptions"]
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


class PRM9012019Rule98o22(RuleDefinitionListIndexedBase):
    """Rule 12 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule98o22, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule98o22.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-12",
            description="The baseline system economizer high-limit shutoff shall be a dry-bulb fixed switch with set-point temperatures in accordance with the values in Table G3.1.2.7.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.7",
            is_primary_rule=True,
            list_path="$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "weather": ["climate_zone"],
            },
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        return {"climate_zone": climate_zone}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule98o22.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                },
                precision={
                    "high_limit_temp_b": {
                        "precision": 0.1,
                        "unit": "K",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            climate_zone_b = data["climate_zone"]
            fan_system_b = hvac_b["fan_system"]

            air_economizer_b = fan_system_b.get("air_economizer")

            return air_economizer_b is not None and (
                climate_zone_b in CLIMATE_ZONE_70F or climate_zone_b in CLIMATE_ZONE_75F
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            climate_zone_b = data["climate_zone"]
            fan_system_b = hvac_b["fan_system"]

            high_limit_temp_b = getattr_(
                fan_system_b,
                "fan_system",
                "air_economizer",
                "high_limit_shutoff_temperature",
            )

            air_economizer_type_b = getattr_(
                fan_system_b,
                "fan_system",
                "air_economizer",
                "type",
            )

            if climate_zone_b in CLIMATE_ZONE_70F:
                req_high_limit_temp = 70 * ureg("degF")
            elif climate_zone_b in CLIMATE_ZONE_75F:
                req_high_limit_temp = 75 * ureg("degF")

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
                self.precision_comparison["high_limit_temp_b"](
                    high_limit_temp_b.to(ureg.kelvin),
                    req_high_limit_temp.to(ureg.kelvin),
                )
                and air_economizer_type_b == AIR_ECONOMIZER.TEMPERATURE
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            req_high_limit_temp = calc_vals["req_high_limit_temp"]
            high_limit_temp_b = calc_vals["high_limit_temp_b"]
            air_economizer_type_b = calc_vals["air_economizer_type_b"]

            return (
                std_equal(
                    req_high_limit_temp.to(ureg.kelvin),
                    high_limit_temp_b.to(ureg.kelvin),
                )
                and air_economizer_type_b == AIR_ECONOMIZER.TEMPERATURE
            )
