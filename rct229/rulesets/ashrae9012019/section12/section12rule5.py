from pydash import flatten
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.schedule_utils import get_schedule_multiplier_hourly_value_or_default

END_USE = SchemaEnums.schema_enums["EndUseOptions"]

ACCEPTABLE_RESULT_TYPE = [
    END_USE.MISC_EQUIPMENT,
    END_USE.INDUSTRIAL_PROCESS,
    END_USE.OFFICE_EQUIPMENT,
    END_USE.COMPUTERS_SERVERS,
    END_USE.COMMERCIAL_COOKING,
]


class PRM9012019Rule73v23(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(PRM9012019Rule73v23, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule73v23.RMDRule(),
            index_rmd=PROPOSED,
            id="12-5",
            description="Receptacle and process loads shall always be included in simulations of the building. "
            "These loads shall be included when calculating the proposed building performance and the baseline building performance as required by Section G1.2.1.",
            ruleset_section_title="Receptacle",
            standard_section="Table G3.1-12 Proposed Building Performance column",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule73v23.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule73v23.RMDRule.MiscellaneousEquipmentRule(),
                index_rmd=PROPOSED,
                list_path="buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*]",
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            schedule_eflh_b = sum(
                flatten(
                    [
                        get_schedule_multiplier_hourly_value_or_default(
                            rmd_b,
                            getattr_(
                                misc_equip_b,
                                "miscellaneous_equipment",
                                "multiplier_schedule",
                            ),
                        )
                        for misc_equip_b in find_all(
                            "$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*]",
                            rmd_b,
                        )
                    ]
                ),
                0,
            )

            schedule_eflh_p = sum(
                flatten(
                    [
                        get_schedule_multiplier_hourly_value_or_default(
                            rmd_p,
                            getattr_(
                                misc_equip_p,
                                "miscellaneous_equipment",
                                "multiplier_schedule",
                            ),
                        )
                        for misc_equip_p in find_all(
                            "$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*]",
                            rmd_p,
                        )
                    ]
                ),
                0,
            )

            has_annual_energy_use_b = any(
                [
                    getattr_(annual_end_use_result, "annual_end_use_results", "type")
                    in ACCEPTABLE_RESULT_TYPE
                    and getattr_(
                        annual_end_use_result,
                        "annual_end_use_results",
                        "annual_site_energy_use",
                    )
                    > 0 * ureg("J")
                    for annual_end_use_result in find_all(
                        "$.model_output.annual_end_use_results[*]",
                        rmd_b,
                    )
                ]
            )

            has_annual_energy_use_p = any(
                [
                    getattr_(annual_end_use_result, "annual_end_use_results", "type")
                    in ACCEPTABLE_RESULT_TYPE
                    and getattr_(
                        annual_end_use_result,
                        "annual_end_use_results",
                        "annual_site_energy_use",
                    )
                    > 0 * ureg("J")
                    for annual_end_use_result in find_all(
                        "$.model_output.annual_end_use_results[*]",
                        rmd_p,
                    )
                ]
            )

            return {
                "schedule_eflh_b": schedule_eflh_b,
                "schedule_eflh_p": schedule_eflh_p,
                "has_annual_energy_use_b": has_annual_energy_use_b,
                "has_annual_energy_use_p": has_annual_energy_use_p,
            }

        class MiscellaneousEquipmentRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule73v23.RMDRule.MiscellaneousEquipmentRule,
                    self,
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={"$": ["power"]},
                )

            def get_calc_vals(self, context, data=None):
                misc_equip_b = context.BASELINE_0
                misc_equip_p = context.PROPOSED

                has_annual_energy_use_b = data["has_annual_energy_use_b"]
                schedule_eflh_b = data["schedule_eflh_b"]

                has_annual_energy_use_p = data["has_annual_energy_use_p"]
                schedule_eflh_p = data["schedule_eflh_p"]

                loads_included_b = (
                    misc_equip_b["power"] > 0 * ureg("W")
                    and (
                        misc_equip_b.get("sensible_fraction", 0) > 0
                        or misc_equip_b.get("latent_fraction", 0) > 0
                    )
                    and schedule_eflh_b > 0
                )

                loads_included_p = (
                    misc_equip_p["power"] > 0 * ureg("W")
                    and (
                        misc_equip_p.get("sensible_fraction", 0) > 0
                        or misc_equip_p.get("latent_fraction", 0) > 0
                    )
                    and schedule_eflh_p > 0
                )

                return {
                    "has_annual_energy_use_b": has_annual_energy_use_b,
                    "has_annual_energy_use_p": has_annual_energy_use_p,
                    "loads_included_b": loads_included_b,
                    "loads_included_p": loads_included_p,
                }

            def rule_check(self, context, calc_vals=None, data=None):
                loads_included_b = calc_vals["loads_included_b"]
                loads_included_p = calc_vals["loads_included_p"]
                has_annual_energy_use_b = calc_vals["has_annual_energy_use_b"]
                has_annual_energy_use_p = calc_vals["has_annual_energy_use_p"]

                return (
                    loads_included_b
                    and loads_included_p
                    and has_annual_energy_use_b
                    and has_annual_energy_use_p
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                misc_equip_b = context.BASELINE_0
                misc_equip_p = context.PROPOSED
                loads_included_b = calc_vals["loads_included_b"]
                loads_included_p = calc_vals["loads_included_p"]
                has_annual_energy_use_b = calc_vals["has_annual_energy_use_b"]
                has_annual_energy_use_p = calc_vals["has_annual_energy_use_p"]
                schedule_eflh_b = data["schedule_eflh_b"]
                schedule_eflh_p = data["schedule_eflh_p"]

                FAIL_MSG = " | ".join(
                    filter(
                        None,
                        [
                            (
                                f"Proposed: No misc. loads [power={misc_equip_p['power']}, sens={misc_equip_p.get('sensible_fraction')}, lat={misc_equip_p.get('latent_fraction')}, EFLH={schedule_eflh_p}]"
                                if not loads_included_p
                                else ""
                            ),
                            (
                                "Proposed: No annual end use energy."
                                if not has_annual_energy_use_p
                                else ""
                            ),
                            (
                                f"Baseline: No misc. loads [power={misc_equip_b['power']}, sens={misc_equip_b.get('sensible_fraction')}, lat={misc_equip_b.get('latent_fraction')}, EFLH={schedule_eflh_b}]"
                                if not loads_included_b
                                else ""
                            ),
                            (
                                "Baseline: No annual end use energy."
                                if not has_annual_energy_use_b
                                else ""
                            ),
                        ],
                    )
                )

                return FAIL_MSG
