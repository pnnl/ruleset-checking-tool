from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import PROPOSED
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.utility_functions import find_exactly_one_schedule

SPACE_FUNCTION = SchemaEnums.schema_enums["SpaceFunctionOptions"]


class PRM9012022rule12d80(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2022 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012022rule12d80, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012022rule12d80.SpaceRule(),
            index_rmd=PROPOSED,
            id="6-10",
            description="Lighting and miscellaneous equipment loads and schedules are modeled identically across the baseline and proposed for plenums, crawl spaces, and interstitial spaces.",
            ruleset_section_title="Lighting",
            standard_section="able G3.1 #1 Baseline Column",
            is_primary_rule=True,
            list_path="$.buildings[*].building_segments[*].zones[*].spaces[*]",
            rmd_context="ruleset_model_descriptions/0",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        ltg_schedule_b = {
            int_ltg_sch_id_b: find_exactly_one_schedule(rmd_b, int_ltg_sch_id_b)
            for int_ltg_sch_id_b in find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*].interior_lighting[*].ltg_multiplier_schedule",
                rmd_b,
            )
        }
        ltg_schedule_p = {
            int_ltg_sch_id_p: find_exactly_one_schedule(rmd_b, int_ltg_sch_id_p)
            for int_ltg_sch_id_p in find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*].interior_lighting[*].ltg_multiplier_schedule",
                rmd_p,
            )
        }

        equip_schedule_b = {
            equip_ltg_sch_id_b: find_exactly_one_schedule(rmd_b, equip_ltg_sch_id_b)
            for equip_ltg_sch_id_b in find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].multiplier_schedule",
                rmd_b,
            )
        }
        equip_schedule_p = {
            equip_ltg_sch_id_p: find_exactly_one_schedule(rmd_b, equip_ltg_sch_id_p)
            for equip_ltg_sch_id_p in find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].multiplier_schedule",
                rmd_p,
            )
        }

        return {
            "ltg_schedule_b": ltg_schedule_b,
            "ltg_schedule_p": ltg_schedule_p,
            "equip_schedule_b": equip_schedule_b,
            "equip_schedule_p": equip_schedule_p,
        }

    class SpaceRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012022rule12d80.SpaceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={
                    "$": ["function"],
                },
            )

        def is_applicable(self, context, data=None):
            space_p = context.PROPOSED

            return space_p["function"] not in (
                SPACE_FUNCTION.PLENUM,
                SPACE_FUNCTION.CRAWL_SPACE,
                SPACE_FUNCTION.INTERSTITIAL_SPACE,
            )

        def get_calc_vals(self, context, data=None):
            space_b = context.BASELINE_0
            space_p = context.PROPOSED

            ltg_schedule_b = data["ltg_schedule_b"]
            ltg_schedule_p = data["ltg_schedule_p"]
            equip_schedule_b = data["equip_schedule_b"]
            equip_schedule_p = data["equip_schedule_p"]

            int_ltg_mismatch = False
            ltg_purpose_type_match = False
            ltg_power_per_area_match = False
            for int_ltg_p in space_p.get("interior_lighting", []):
                int_ltg_b = find_exactly_one_with_field_value(
                    "$.interior_lighting[*]", "id", int_ltg_p["id"], space_b
                )
                if (
                    int_ltg_b.get("purpose_type") != int_ltg_b.get("purpose_type")
                    or int_ltg_b.get("power_per_area")
                    != int_ltg_p.get("power_per_area")
                    or int_ltg_b.get("occupancy_control_type")
                    != int_ltg_p.get("occupancy_control_type")
                    or int_ltg_b.get("dayltg_control_type")
                    != int_ltg_p.get("dayltg_control_type")
                    or ltg_schedule_b[int_ltg_b.get("ltg_multiplier_schedule")]
                    != ltg_schedule_p[int_ltg_p.get("ltg_multiplier_schedule")]
                ):
                    int_ltg_mismatch = True

            mis_equip_mismatch = False
            for mis_equip_p in space_p.get("miscellaneous_equipment", []):
                mis_equip_b = find_exactly_one_with_field_value(
                    "$.miscellaneous_equipment[*]", "id", mis_equip_p["id"], space_b
                )
                if (
                    mis_equip_b.get("energy_type") != mis_equip_p.get("energy_type")
                    or mis_equip_b.get("power") != mis_equip_p.get("power")
                    or mis_equip_b.get("sensible_fraction")
                    != mis_equip_p.get("sensible_fraction")
                    or mis_equip_b.get("latent_fraction")
                    != mis_equip_p.get("latent_fraction")
                    or mis_equip_b.get("remaining_fraction_to_loop")
                    != mis_equip_p.get("remaining_fraction_to_loop")
                    or mis_equip_b.get("energy_from_loop")
                    != mis_equip_p.get("energy_from_loop")
                    or mis_equip_b.get("type") != mis_equip_p.get("type")
                    or mis_equip_b.get("automatic_controlled_percentage")
                    != mis_equip_p.get("automatic_controlled_percentage")
                    or equip_schedule_b[mis_equip_b.get("multiplier_schedule")]
                    != equip_schedule_p[mis_equip_p.get("multiplier_schedule")]
                ):
                    mis_equip_mismatch = True

            return {
                "int_ltg_mismatch": int_ltg_mismatch,
                "mis_equip_mismatch": mis_equip_mismatch,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            int_ltg_mismatch = calc_vals["int_ltg_mismatch"]
            mis_equip_mismatch = calc_vals["mis_equip_mismatch"]

            return not (int_ltg_mismatch and mis_equip_mismatch)

        def fail_validation(self, context, calc_vals=None, data=None):
            space_b = context.BASELINE_0
            space_p = context.PROPOSED

            fail_msg = (
                f"It is expected that lighting and miscelleneous equipment would be modeled identically "
                f"across the baseline and proposed for plenums, crawl spaces, and interstitial spaces. A mismatch was observed for {space_p}"
            )

            return fail_msg
