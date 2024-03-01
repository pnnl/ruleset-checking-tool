from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_one_with_field_value
from rct229.utils.pint_utils import ZERO, CalcQ

CONDITIONED_ZONE_TYPE = [
    ZCC.CONDITIONED_MIXED,
    ZCC.CONDITIONED_NON_RESIDENTIAL,
    ZCC.CONDITIONED_RESIDENTIAL,
]
MANUAL_CHECK_MSG = "There is a temperature schedule mismatch between the baseline and proposed rmrs. Fail unless Table G3.1 #4 baseline column exception #s 1 and/or 2 are applicable"


class Section4Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 4 (Airside System)"""

    def __init__(self):
        super(Section4Rule1, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section4Rule1.RuleSetModelInstanceRule(),
            index_rmr=BASELINE_0,
            id="4-1",
            description="Temperature Control Setpoints shall be the same for proposed design and baseline building design.",
            ruleset_section_title="Airside System",
            standard_section="Section G3.1-4 Schedule Modeling Requirements for the Proposed design and Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section4Rule1.RuleSetModelInstanceRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section4Rule1.RuleSetModelInstanceRule.BuildingRule(),
                index_rmr=BASELINE_0,
                list_path="$.buildings[*]",
                required_fields={"$": ["schedules"]},
            )

        def create_data(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            return {
                "schedules_b": rmd_b["schedules"],
                "schedules_p": rmd_p["schedules"],
            }

        class BuildingRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    Section4Rule1.RuleSetModelInstanceRule.BuildingRule, self
                ).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    each_rule=Section4Rule1.RuleSetModelInstanceRule.BuildingRule.ZoneRule(),
                    index_rmr=BASELINE_0,
                    list_path="$.building_segments[*].zones[*]",
                )

            def create_data(self, context, data=None):
                building_b = context.BASELINE_0
                return {
                    "zcc_dict_b": get_zone_conditioning_category_dict(
                        data["climate_zone"], building_b
                    ),
                }

            def list_filter(self, context_item, data=None):
                zcc_dict_b = data["zcc_dict_b"]
                zone_b = context_item.BASELINE_0
                return zcc_dict_b[zone_b["id"]] in CONDITIONED_ZONE_TYPE

            class ZoneRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section4Rule1.RuleSetModelInstanceRule.BuildingRule.ZoneRule,
                        self,
                    ).__init__(
                        rmrs_used=produce_ruleset_model_instance(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                        manual_check_required_msg=MANUAL_CHECK_MSG,
                    )

                def get_calc_vals(self, context, data=None):
                    zone_b = context.BASELINE_0
                    zone_p = context.PROPOSED

                    schedules_b = data["schedules_b"]
                    schedules_p = data["schedules_p"]

                    thermostat_cooling_stpt_sch_id_b = zone_b.get(
                        "thermostat_cooling_setpoint_schedule"
                    )
                    thermostat_cooling_stpt_sch_id_p = zone_p.get(
                        "thermostat_cooling_setpoint_schedule"
                    )

                    design_thermostat_cooling_stpt_b = (
                        zone_b.getattr_(zone_b, "design_thermostat_cooling_setpoint")
                        if not thermostat_cooling_stpt_sch_id_b
                        else ZERO.TEMPERATURE
                    )
                    design_thermostat_cooling_stpt_p = (
                        zone_p.getattr_(zone_p, "design_thermostat_cooling_setpoint")
                        if not thermostat_cooling_stpt_sch_id_p
                        else ZERO.TEMPERATURE
                    )

                    thermostat_cooling_stpt_houlry_values_b = (
                        getattr_(
                            find_one_with_field_value(
                                "$[*]",
                                "id",
                                thermostat_cooling_stpt_sch_id_b,
                                schedules_b,
                            ),
                            "schedules",
                            "hourly_values",
                        )
                        if thermostat_cooling_stpt_sch_id_b
                        else None
                    )

                    thermostat_cooling_stpt_houlry_values_p = (
                        getattr_(
                            find_one_with_field_value(
                                "$[*]",
                                "id",
                                thermostat_cooling_stpt_sch_id_p,
                                schedules_p,
                            ),
                            "schedules",
                            "hourly_values",
                        )
                        if thermostat_cooling_stpt_sch_id_b
                        else None
                    )

                    thermostat_heating_stpt_sch_id_b = zone_b.get(
                        "thermostat_heating_setpoint_schedule"
                    )
                    thermostat_heating_stpt_sch_id_p = zone_p.get(
                        "thermostat_heating_setpoint_schedule"
                    )

                    design_thermostat_heating_stpt_b = (
                        zone_b.getattr_(zone_b, "design_thermostat_heating_setpoint")
                        if not thermostat_heating_stpt_sch_id_b
                        else ZERO.TEMPERATURE
                    )
                    design_thermostat_heating_stpt_p = (
                        zone_p.getattr_(zone_p, "design_thermostat_heating_setpoint")
                        if not thermostat_heating_stpt_sch_id_p
                        else ZERO.TEMPERATURE
                    )

                    thermostat_heating_stpt_houlry_values_b = (
                        getattr_(
                            find_one_with_field_value(
                                "$[*]",
                                "id",
                                thermostat_heating_stpt_sch_id_b,
                                schedules_b,
                            ),
                            "schedules",
                            "hourly_values",
                        )
                        if thermostat_heating_stpt_sch_id_b
                        else None
                    )

                    thermostat_heating_stpt_houlry_values_p = (
                        getattr_(
                            find_one_with_field_value(
                                "$[*]",
                                "id",
                                thermostat_heating_stpt_sch_id_p,
                                schedules_p,
                            ),
                            "schedules",
                            "hourly_values",
                        )
                        if thermostat_heating_stpt_sch_id_b
                        else None
                    )

                    return {
                        "thermostat_cooling_stpt_sch_id_b": thermostat_cooling_stpt_sch_id_b,
                        "thermostat_cooling_stpt_sch_id_p": thermostat_cooling_stpt_sch_id_p,
                        "thermostat_cooling_stpt_houlry_values_b": thermostat_cooling_stpt_houlry_values_b,
                        "thermostat_cooling_stpt_houlry_values_p": thermostat_cooling_stpt_houlry_values_p,
                        "design_thermostat_cooling_stpt_b": CalcQ(
                            "temperature", design_thermostat_cooling_stpt_b
                        ),
                        "design_thermostat_cooling_stpt_p": CalcQ(
                            "temperature", design_thermostat_cooling_stpt_p
                        ),
                        "thermostat_heating_stpt_sch_id_b": thermostat_heating_stpt_sch_id_b,
                        "thermostat_heating_stpt_sch_id_p": thermostat_heating_stpt_sch_id_p,
                        "thermostat_heating_stpt_houlry_values_b": thermostat_heating_stpt_houlry_values_b,
                        "thermostat_heating_stpt_houlry_values_p": thermostat_heating_stpt_houlry_values_p,
                        "design_thermostat_heating_stpt_b": CalcQ(
                            "temperature", design_thermostat_heating_stpt_b
                        ),
                        "design_thermostat_heating_stpt_p": CalcQ(
                            "temperature", design_thermostat_heating_stpt_p
                        ),
                    }

                def manual_check_required(self, context, calc_vals=None, data=None):
                    thermostat_cooling_stpt_sch_id_b = calc_vals[
                        "thermostat_cooling_stpt_sch_id_b"
                    ]
                    thermostat_cooling_stpt_sch_id_p = calc_vals[
                        "thermostat_cooling_stpt_sch_id_p"
                    ]
                    thermostat_cooling_stpt_houlry_values_b = calc_vals[
                        "thermostat_cooling_stpt_houlry_values_b"
                    ]
                    thermostat_cooling_stpt_houlry_values_p = calc_vals[
                        "thermostat_cooling_stpt_houlry_values_p"
                    ]

                    thermostat_heating_stpt_sch_id_b = calc_vals[
                        "thermostat_heating_stpt_sch_id_b"
                    ]
                    thermostat_heating_stpt_sch_id_p = calc_vals[
                        "thermostat_heating_stpt_sch_id_p"
                    ]
                    thermostat_heating_stpt_houlry_values_b = calc_vals[
                        "thermostat_heating_stpt_houlry_values_b"
                    ]
                    thermostat_heating_stpt_houlry_values_p = calc_vals[
                        "thermostat_heating_stpt_houlry_values_p"
                    ]
                    return (
                        thermostat_cooling_stpt_sch_id_b
                        and thermostat_cooling_stpt_sch_id_p
                        and thermostat_cooling_stpt_houlry_values_b
                        != thermostat_cooling_stpt_houlry_values_p
                    ) or (
                        thermostat_heating_stpt_sch_id_b
                        and thermostat_heating_stpt_sch_id_p
                        and thermostat_heating_stpt_houlry_values_b
                        != thermostat_heating_stpt_houlry_values_p
                    )

                def rule_check(self, context, calc_vals=None, data=None):
                    thermostat_cooling_stpt_sch_id_b = calc_vals[
                        "thermostat_cooling_stpt_sch_id_b"
                    ]
                    thermostat_cooling_stpt_sch_id_p = calc_vals[
                        "thermostat_cooling_stpt_sch_id_p"
                    ]
                    thermostat_cooling_stpt_houlry_values_b = calc_vals[
                        "thermostat_cooling_stpt_houlry_values_b"
                    ]
                    thermostat_cooling_stpt_houlry_values_p = calc_vals[
                        "thermostat_cooling_stpt_houlry_values_p"
                    ]
                    design_thermostat_cooling_stpt_b = calc_vals[
                        "design_thermostat_cooling_stpt_b"
                    ]
                    design_thermostat_cooling_stpt_p = calc_vals[
                        "design_thermostat_cooling_stpt_p"
                    ]

                    thermostat_heating_stpt_sch_id_b = calc_vals[
                        "thermostat_heating_stpt_sch_id_b"
                    ]
                    thermostat_heating_stpt_sch_id_p = calc_vals[
                        "thermostat_heating_stpt_sch_id_p"
                    ]
                    thermostat_heating_stpt_houlry_values_b = calc_vals[
                        "thermostat_heating_stpt_houlry_values_b"
                    ]
                    thermostat_heating_stpt_houlry_values_p = calc_vals[
                        "thermostat_heating_stpt_houlry_values_p"
                    ]
                    design_thermostat_heating_stpt_b = calc_vals[
                        "design_thermostat_heating_stpt_b"
                    ]
                    design_thermostat_heating_stpt_p = calc_vals[
                        "design_thermostat_heating_stpt_p"
                    ]
                    return (
                        (
                            thermostat_cooling_stpt_sch_id_b
                            and thermostat_cooling_stpt_sch_id_p
                            and thermostat_cooling_stpt_houlry_values_b
                            == thermostat_cooling_stpt_houlry_values_p
                        )
                        or (
                            not thermostat_cooling_stpt_sch_id_b
                            and not thermostat_cooling_stpt_sch_id_p
                            and design_thermostat_cooling_stpt_b
                            == design_thermostat_cooling_stpt_p
                        )
                    ) and (
                        (
                            thermostat_heating_stpt_sch_id_b
                            and thermostat_heating_stpt_sch_id_p
                            and thermostat_heating_stpt_houlry_values_b
                            == thermostat_heating_stpt_houlry_values_p
                        )
                        or (
                            not thermostat_heating_stpt_sch_id_b
                            and not thermostat_heating_stpt_sch_id_p
                            and design_thermostat_heating_stpt_b
                            == design_thermostat_heating_stpt_p
                        )
                    )
