from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.utility_functions import find_exactly_one_schedule

SPACE_FUNCTION = SchemaEnums.schema_enums["SpaceFunctionOptions"]


class PRM9012022Rule12d80(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012022Rule12d80, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012022Rule12d80.SpaceRule(),
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
                "$.buildings[*].building_segments[*].zones[*].spaces[*].interior_lighting[*].lighting_multiplier_schedule",
                rmd_b,
            )
        }
        ltg_schedule_p = {
            int_ltg_sch_id_p: find_exactly_one_schedule(rmd_p, int_ltg_sch_id_p)
            for int_ltg_sch_id_p in find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*].interior_lighting[*].lighting_multiplier_schedule",
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
            equip_ltg_sch_id_p: find_exactly_one_schedule(rmd_p, equip_ltg_sch_id_p)
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
            super(PRM9012022Rule12d80.SpaceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={
                    "$": ["function", "interior_lighting", "miscellaneous_equipment"],
                    "$.interior_lighting[*]": [
                        "purpose_type",
                        "occupancy_control_type",
                        "daylighting_control_type",
                        "lighting_multiplier_schedule",
                        "power_per_area",
                    ],
                    "$.miscellaneous_equipment[*]": [
                        "energy_type",
                        "power",
                        "sensible_fraction",
                        "latent_fraction",
                        "remaining_fraction_to_loop",
                        "energy_from_loop",
                        "type",
                        "automatic_controlled_percentage",
                        "multiplier_schedule",
                    ],
                },
            )

        def is_applicable(self, context, data=None):
            space_p = context.PROPOSED

            return space_p["function"] in (
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

            ltg_purpose_type_match = True
            ltg_power_per_area_match = True
            ltg_occupancy_control_type_match = True
            ltg_daylighting_control_type_match = True
            ltg_ltg_multiplier_schedule_match = True
            for int_ltg_p in space_p["interior_lighting"]:
                int_ltg_b = find_exactly_one_with_field_value(
                    "$.interior_lighting[*]", "id", int_ltg_p["id"], space_b
                )

                # Start checking whether the lighting keys are the same
                if ltg_purpose_type_match:
                    ltg_purpose_type_match = (
                        int_ltg_b["purpose_type"] == int_ltg_b["purpose_type"]
                    )
                if ltg_power_per_area_match:
                    ltg_power_per_area_match = (
                        int_ltg_b["power_per_area"] == int_ltg_p["power_per_area"]
                    )
                if ltg_occupancy_control_type_match:
                    ltg_occupancy_control_type_match = (
                        int_ltg_b["occupancy_control_type"]
                        == int_ltg_p["occupancy_control_type"]
                    )
                if ltg_daylighting_control_type_match:
                    ltg_daylighting_control_type_match = (
                        int_ltg_b["daylighting_control_type"]
                        == int_ltg_p["daylighting_control_type"]
                    )
                if ltg_ltg_multiplier_schedule_match:
                    ltg_ltg_multiplier_schedule_match = (
                        ltg_schedule_b[int_ltg_b["lighting_multiplier_schedule"]]
                        == ltg_schedule_p[int_ltg_p["lighting_multiplier_schedule"]]
                    )

            mis_equip_energy_type_match = True
            mis_equip_power_match = True
            mis_equip_sensible_fraction_match = True
            mis_equip_latent_fraction_match = True
            mis_equip_remaining_fraction_to_loop_match = True
            mis_equip_energy_from_loop_match = True
            mis_equip_type_match = True
            mis_equip_automatic_controlled_percentage_match = True
            mis_equip_multiplier_schedule_match = True
            for mis_equip_p in space_p["miscellaneous_equipment"]:
                mis_equip_b = find_exactly_one_with_field_value(
                    "$.miscellaneous_equipment[*]", "id", mis_equip_p["id"], space_b
                )

                # Start checking whether the equipment keys are the same
                if mis_equip_energy_type_match:
                    mis_equip_energy_type_match = (
                        mis_equip_b["energy_type"] == mis_equip_p["energy_type"]
                    )
                if mis_equip_power_match:
                    mis_equip_power_match = mis_equip_b["power"] == mis_equip_p["power"]
                if mis_equip_sensible_fraction_match:
                    mis_equip_sensible_fraction_match = (
                        mis_equip_b["sensible_fraction"]
                        == mis_equip_p["sensible_fraction"]
                    )
                if mis_equip_latent_fraction_match:
                    mis_equip_latent_fraction_match = (
                        mis_equip_b["latent_fraction"] == mis_equip_p["latent_fraction"]
                    )
                if mis_equip_remaining_fraction_to_loop_match:
                    mis_equip_remaining_fraction_to_loop_match = (
                        mis_equip_b["remaining_fraction_to_loop"]
                        == mis_equip_p["remaining_fraction_to_loop"]
                    )
                if mis_equip_energy_from_loop_match:
                    mis_equip_energy_from_loop_match = (
                        mis_equip_b["energy_from_loop"]
                        == mis_equip_p["energy_from_loop"]
                    )
                if mis_equip_type_match:
                    mis_equip_type_match = mis_equip_b["type"] == mis_equip_p["type"]
                if mis_equip_automatic_controlled_percentage_match:
                    mis_equip_automatic_controlled_percentage_match = (
                        mis_equip_b["automatic_controlled_percentage"]
                        == mis_equip_p["automatic_controlled_percentage"]
                    )
                if mis_equip_multiplier_schedule_match:
                    mis_equip_multiplier_schedule_match = (
                        equip_schedule_b[mis_equip_b["multiplier_schedule"]]
                        == equip_schedule_p[mis_equip_p["multiplier_schedule"]]
                    )

            return {
                "ltg_purpose_type_match": ltg_purpose_type_match,
                "ltg_power_per_area_match": ltg_power_per_area_match,
                "ltg_occupancy_control_type_match": ltg_occupancy_control_type_match,
                "ltg_daylighting_control_type_match": ltg_daylighting_control_type_match,
                "ltg_ltg_multiplier_schedule_match": ltg_ltg_multiplier_schedule_match,
                "mis_equip_energy_type_match": mis_equip_energy_type_match,
                "mis_equip_power_match": mis_equip_power_match,
                "mis_equip_sensible_fraction_match": mis_equip_sensible_fraction_match,
                "mis_equip_latent_fraction_match": mis_equip_latent_fraction_match,
                "mis_equip_remaining_fraction_to_loop_match": mis_equip_remaining_fraction_to_loop_match,
                "mis_equip_energy_from_loop_match": mis_equip_energy_from_loop_match,
                "mis_equip_type_match": mis_equip_type_match,
                "mis_equip_automatic_controlled_percentage_match": mis_equip_automatic_controlled_percentage_match,
                "mis_equip_multiplier_schedule_match": mis_equip_multiplier_schedule_match,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            ltg_purpose_type_match = calc_vals["ltg_purpose_type_match"]
            ltg_power_per_area_match = calc_vals["ltg_power_per_area_match"]

            ltg_occupancy_control_type_match = calc_vals[
                "ltg_occupancy_control_type_match"
            ]
            ltg_daylighting_control_type_match = calc_vals[
                "ltg_daylighting_control_type_match"
            ]
            ltg_ltg_multiplier_schedule_match = calc_vals[
                "ltg_ltg_multiplier_schedule_match"
            ]
            mis_equip_energy_type_match = calc_vals["mis_equip_energy_type_match"]

            mis_equip_power_match = calc_vals["mis_equip_power_match"]
            mis_equip_sensible_fraction_match = calc_vals[
                "mis_equip_sensible_fraction_match"
            ]
            mis_equip_latent_fraction_match = calc_vals[
                "mis_equip_latent_fraction_match"
            ]
            mis_equip_remaining_fraction_to_loop_match = calc_vals[
                "mis_equip_remaining_fraction_to_loop_match"
            ]
            mis_equip_energy_from_loop_match = calc_vals[
                "mis_equip_energy_from_loop_match"
            ]
            mis_equip_type_match = calc_vals["mis_equip_type_match"]
            mis_equip_automatic_controlled_percentage_match = calc_vals[
                "mis_equip_automatic_controlled_percentage_match"
            ]
            mis_equip_multiplier_schedule_match = calc_vals[
                "mis_equip_multiplier_schedule_match"
            ]

            return (
                ltg_purpose_type_match
                and ltg_power_per_area_match
                and ltg_occupancy_control_type_match
                and ltg_daylighting_control_type_match
                and ltg_ltg_multiplier_schedule_match
                and mis_equip_energy_type_match
                and mis_equip_power_match
                and mis_equip_sensible_fraction_match
                and mis_equip_latent_fraction_match
                and mis_equip_remaining_fraction_to_loop_match
                and mis_equip_energy_from_loop_match
                and mis_equip_type_match
                and mis_equip_automatic_controlled_percentage_match
                and mis_equip_multiplier_schedule_match
            )

        def get_fail_msg(self, context, calc_vals=None, data=None):
            space_p = context.PROPOSED
            space_id_p = space_p["id"]

            ltg_purpose_type_match = calc_vals["ltg_purpose_type_match"]
            ltg_power_per_area_match = calc_vals["ltg_power_per_area_match"]

            ltg_occupancy_control_type_match = calc_vals[
                "ltg_occupancy_control_type_match"
            ]
            ltg_daylighting_control_type_match = calc_vals[
                "ltg_daylighting_control_type_match"
            ]
            ltg_ltg_multiplier_schedule_match = calc_vals[
                "ltg_ltg_multiplier_schedule_match"
            ]
            mis_equip_energy_type_match = calc_vals["mis_equip_energy_type_match"]
            mis_equip_power_match = calc_vals["mis_equip_power_match"]
            mis_equip_sensible_fraction_match = calc_vals[
                "mis_equip_sensible_fraction_match"
            ]
            mis_equip_latent_fraction_match = calc_vals[
                "mis_equip_latent_fraction_match"
            ]
            mis_equip_remaining_fraction_to_loop_match = calc_vals[
                "mis_equip_remaining_fraction_to_loop_match"
            ]
            mis_equip_energy_from_loop_match = calc_vals[
                "mis_equip_energy_from_loop_match"
            ]
            mis_equip_type_match = calc_vals["mis_equip_type_match"]
            mis_equip_automatic_controlled_percentage_match = calc_vals[
                "mis_equip_automatic_controlled_percentage_match"
            ]
            mis_equip_multiplier_schedule_match = calc_vals[
                "mis_equip_multiplier_schedule_match"
            ]

            mismatch = " ".join(
                criteria
                for criteria, match in [
                    ("purpose_type", ltg_purpose_type_match),
                    ("power_per_area", ltg_power_per_area_match),
                    ("occupancy_control_type", ltg_occupancy_control_type_match),
                    ("daylighting_control_type", ltg_daylighting_control_type_match),
                    ("lighting_multiplier_schedule", ltg_ltg_multiplier_schedule_match),
                    ("energy_type", mis_equip_energy_type_match),
                    ("mis_equip_power_match", mis_equip_power_match),
                    ("sensible_fraction", mis_equip_sensible_fraction_match),
                    ("latent_fraction", mis_equip_latent_fraction_match),
                    (
                        "remaining_fraction_to_loop",
                        mis_equip_remaining_fraction_to_loop_match,
                    ),
                    ("energy_from_loop", mis_equip_energy_from_loop_match),
                    ("type", mis_equip_type_match),
                    (
                        "automatic_controlled_percentage",
                        mis_equip_automatic_controlled_percentage_match,
                    ),
                    ("multiplier_schedule", mis_equip_multiplier_schedule_match),
                ]
                if not match
            )

            fail_msg = (
                f"It is expected that lighting and miscelleneous equipment would be modeled identically "
                f"across the baseline and proposed for plenums, crawl spaces, and interstitial spaces. A mismatch was observed for {space_id_p} and {mismatch}"
            )

            return fail_msg
