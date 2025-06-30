from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
)

HUMIDIFICATION = SchemaEnums.schema_enums["HumidificationOptions"]


class PRM9012019Rule34l34(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 10 (HVAC General)"""

    def __init__(self):
        super(PRM9012019Rule34l34, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule34l34.ZoneRule(),
            index_rmd=BASELINE_0,
            id="10-1",
            description="When the proposed design includes humidification and complies with Section 6.5.2.4, then the baseline building design shall use nonadiabatic humidification. "
            "When the proposed design includes humidification and does not comply with Section 6.5.2.4 then the baseline building design shall use adiabatic humidification.",
            ruleset_section_title="HVAC General",
            standard_section="Section G3.1-10 HVAC Systems for the baseline building",
            is_primary_rule=True,
            list_path="$.buildings[*].building_segments[*].zones[*]",
            rmd_context="ruleset_model_descriptions/0",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        hvac_zone_list_w_area_dict_p = get_hvac_zone_list_w_area_by_rmd_dict(rmd_p)

        zones_have_humidification_list_p = []
        for hvac_p in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            rmd_p,
        ):
            if hvac_p.get("humidification_type") not in (None, HUMIDIFICATION.NONE):
                zone_list_p = hvac_zone_list_w_area_dict_p[hvac_p["id"]]["zone_list"]
                zones_have_humidification_list_p.extend(zone_list_p)

        zones_have_humidification_list_p = list(set(zones_have_humidification_list_p))

        zone_has_humidification_dict_b = {}
        zone_has_humidification_dict_p = {}
        for zone_b in find_all("$.buildings[*].building_segments[*].zones[*]", rmd_b):
            zone_id_b = zone_b["id"]
            hvac_list_b = get_list_hvac_systems_associated_with_zone(rmd_b, zone_id_b)

            assert_(
                len(hvac_list_b) == 1,
                "There must be only one HVAC system serving each zone in the baseline RMD.",
            )

            zone_has_humidification_dict_b[zone_id_b] = find_exactly_one_hvac_system(
                rmd_b, hvac_list_b[0]
            ).get("humidification_type") not in (None, HUMIDIFICATION.NONE)
            zone_has_humidification_dict_p[zone_id_b] = (
                zone_b["id"] in zones_have_humidification_list_p
            )

        return {
            "zone_has_humidification_dict_b": zone_has_humidification_dict_b,
            "zone_has_humidification_dict_p": zone_has_humidification_dict_p,
        }

    class ZoneRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule34l34.ZoneRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
            )

        def get_calc_vals(self, context, data=None):
            zone_b = context.BASELINE_0
            zone_id_b = zone_b["id"]

            zone_has_humidification_bool_b = data["zone_has_humidification_dict_b"][
                zone_id_b
            ]
            zone_has_humidification_bool_p = data["zone_has_humidification_dict_p"][
                zone_id_b
            ]

            return {
                "zone_has_humidification_bool_b": zone_has_humidification_bool_b,
                "zone_has_humidification_bool_p": zone_has_humidification_bool_p,
            }

        def applicability_check(self, context, calc_vals, data):
            zone_has_humidification_bool_b = calc_vals["zone_has_humidification_bool_b"]
            zone_has_humidification_bool_p = calc_vals["zone_has_humidification_bool_p"]

            return zone_has_humidification_bool_b and zone_has_humidification_bool_p

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            zone_has_humidification_bool_b = calc_vals["zone_has_humidification_bool_b"]
            zone_has_humidification_bool_p = calc_vals["zone_has_humidification_bool_p"]

            UNDETERMINED_MSG = ""
            if zone_has_humidification_bool_b and zone_has_humidification_bool_p:
                UNDETERMINED_MSG = (
                    "This zone is modeled with humidification in the baseline and proposed. Check that the baseline system serving this zone is modeled with adiabatic humidification "
                    "if the specified humidification system complies with 90.1 - 2019 Section 6.5.2.4, and that the baseline system serving this zone is modeled with non-adiabatic humidification "
                    "if the specified system does not comply with Section 6.5.2.4. Note, for informational purposes, there is a separate rule that verifies that the baseline is modeled with humidification when the proposed design has humidification."
                )

            return UNDETERMINED_MSG
