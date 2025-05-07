from rct229.rule_engine.rule_base import RuleDefinitionBase
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
from rct229.utils.utility_functions import find_exactly_one_hvac_system

HUMIDIFICATION = SchemaEnums.schema_enums["HumidificationOptions"]


class Section10Rule15(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 10 (HVAC General)"""

    def __init__(self):
        super(Section10Rule15, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section10Rule15.ZoneRule(),
            index_rmd=BASELINE_0,
            id="10-15",
            description="The proposed design includes humidification and the baseline building design has been modeled with humidification.",
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

        has_humidification_b = {}
        has_humidification_p = {}
        for zone_b in find_all("$.buildings[*].building_segments[*].zones[*]", rmd_b):
            zone_id_b = zone_b["id"]
            hvac_list_b = get_list_hvac_systems_associated_with_zone(rmd_b, zone_id_b)

            assert_(
                len(hvac_list_b) == 1,
                "There must be one system serving each zone in the baseline RMD.",
            )

            has_humidification_b[zone_id_b] = find_exactly_one_hvac_system(
                rmd_b, hvac_list_b[0]
            ).get("humidification_type") not in (None, HUMIDIFICATION.NONE)
            has_humidification_p[zone_id_b] = (
                zone_b["id"] in zones_have_humidification_list_p
            )

        return {
            "has_humidification_b": has_humidification_b,
            "has_humidification_p": has_humidification_p,
        }

    class ZoneRule(RuleDefinitionBase):
        def __init__(self):
            super(Section10Rule15.ZoneRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
            )

        def is_applicable(self, context, data=None):
            zone_b = context.BASELINE_0
            zone_id_b = zone_b["id"]

            has_humidification_b = data["has_humidification_b"][zone_id_b]
            has_humidification_p = data["has_humidification_p"][zone_id_b]

            # if one or two of the variables are True, the rule is applicable
            return has_humidification_b or has_humidification_p

        def get_calc_vals(self, context, data=None):
            zone_b = context.BASELINE_0
            zone_id_b = zone_b["id"]

            has_humidification_b = data["has_humidification_b"][zone_id_b]
            has_humidification_p = data["has_humidification_p"][zone_id_b]

            return {
                "has_humidification_b": has_humidification_b,
                "has_humidification_p": has_humidification_p,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            has_humidification_b = calc_vals["has_humidification_b"]
            has_humidification_p = calc_vals["has_humidification_p"]

            return has_humidification_b and has_humidification_p

        def get_fail_msg(self, context, calc_vals=None, data=None):
            has_humidification_b = calc_vals["has_humidification_b"]
            has_humidification_p = calc_vals["has_humidification_p"]

            FAIL_MSG = ""
            if has_humidification_b and not has_humidification_p:
                FAIL_MSG = "The baseline was modeled with humidification when humidification was not modeled in the proposed design model."
            elif not has_humidification_b and has_humidification_p:
                FAIL_MSG = "The baseline was NOT modeled with humidification when humidification was modeled in the proposed design model."

            return FAIL_MSG
