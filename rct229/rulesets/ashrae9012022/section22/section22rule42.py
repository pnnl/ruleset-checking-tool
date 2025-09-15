from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012022.data_fns.table_J_6_fns import table_J_6_lookup
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums

ENERGY_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]
CHILLER_COMPRESSOR = SchemaEnums.schema_enums["ChillerCompressorOptions"]


class PRM9012022Rule34d03(RuleDefinitionListIndexedBase):
    """Rule 42 of ASHRAE 90.1-2022 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012022Rule34d03, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012022Rule34d03.ChillerRule(),
            index_rmd=BASELINE_0,
            id="22-42",
            description="The sets of performance curves specified in Table J-2 should be used to represent part-load performance of chillers in the baseline building design.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.2.2.1 Baseline",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="chillers[*]",
        )

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012022Rule34d03.ChillerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={"$": ["rated_capacity", "compressor_type"]},
                precision={
                    "chiller_part_load_efficiency": {
                        "precision": 0.001,
                    },
                },
            )

        def is_applicable(self, context, data=None):
            chiller_b = context.BASELINE_0

            return (
                chiller_b.get("condensing_loop") is not None
                and chiller_b.get("energy_source_type") == ENERGY_SOURCE.ELECTRICITY
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.BASELINE_0

            rated_capacity_b = chiller_b["rated_capacity"]
            if chiller_b["compressor_type"] == CHILLER_COMPRESSOR.CENTRIFUGAL:
                if rated_capacity_b < 150 * ureg("ton"):
                    curve_set = "Z"
                elif 150 * ureg("ton") <= rated_capacity_b < 300 * ureg("ton"):
                    curve_set = "AA"
                else:
                    curve_set = "AB"
            elif chiller_b["compressor_type"] in (
                "POSITIVE_DISPLACEMENT",
                "SCROLL",
                "SCREW",
            ):
                if rated_capacity_b < 150 * ureg("ton"):
                    curve_set = "V"
                elif rated_capacity_b > 300 * ureg("ton"):
                    curve_set = "Y"
                else:
                    curve_set = "X"
            else:
                curve_set = None

            if curve_set is not None:
                rated_power = (
                    chiller_b["rated_capacity"] / chiller_b["full_load_efficiency"]
                    if chiller_b.get("full_load_efficiency")
                    else 0.0
                )
                expected_validation_plr = [0.25, 0.5, 0.75, 1]
                expected_chwt_temps = [39, 45, 50, 55]
                expected_ecwt_temps = [60, 104, 85, 72.5, 97.5]
                eir_f_t_coefficients = table_J_6_lookup(curve_set, "EIR-f-T")
                cap_f_t_coefficients = table_J_6_lookup(curve_set, "CAP-f-T")
                plr_coefficients = table_J_6_lookup(curve_set, "EIR-f-PLR")

                capacity_validation_pts_dict = {}
                for capacity_validation_point in chiller_b.get(
                    "capacity_operating_points", []
                ):
                    chilled_water_supply_temp_b = capacity_validation_point.get(
                        "chilled_water_supply_temperature", 0.0 * ureg("degC")
                    ).to("degF")
                    condenser_temp_b = capacity_validation_point.get(
                        "condenser_temperature", 0.0 * ureg("degC")
                    ).to("degF")

                    dict_key = f"{int(round(chilled_water_supply_temp_b.m,1))}, {int(round(condenser_temp_b.m,1))}"
                    capacity_validation_pts_dict[
                        dict_key
                    ] = capacity_validation_point.get("capacity")

                power_validation_pts_dict = {}
                for power_validation_point in chiller_b.get(
                    "power_operating_points", []
                ):
                    chilled_water_supply_temp_b = power_validation_point.get(
                        "chilled_water_supply_temperature", 0.0 * ureg("degC")
                    ).to("degF")
                    condenser_temp_b = power_validation_point.get(
                        "condenser_temperature", 0.0 * ureg("degC")
                    ).to("degF")
                    dict_key = f"{int(round(chilled_water_supply_temp_b.m,1))}, {int(round(condenser_temp_b.m,1))}"

                    power_validation_pts_dict.setdefault(dict_key, [])
                    power_validation_pts_dict[dict_key].append(power_validation_point)

                given_capacities = {}
                missing_capacity_validation_points = []
                non_matching_capacity_validation_points = []
                for chwt in expected_chwt_temps:
                    for ecwt in expected_ecwt_temps:
                        dict_key = f"{chwt}, {ecwt}"
                        if capacity_validation_pts_dict.get(dict_key):
                            expected_capacity = (
                                cap_f_t_coefficients[0]
                                + cap_f_t_coefficients[1] * chwt
                                + cap_f_t_coefficients[2] * chwt**2
                                + cap_f_t_coefficients[3] * ecwt
                                + cap_f_t_coefficients[4] * ecwt**2
                                + cap_f_t_coefficients[5] * chwt * ecwt
                            ) * rated_capacity_b.to("ton")

                            given_capacity = capacity_validation_pts_dict[dict_key]
                            given_capacities[dict_key] = given_capacity

                            if expected_capacity == given_capacity:
                                missing_capacity_validation_points.append(
                                    {"CHWT": chwt, "ECWT": ecwt}
                                )
                            else:
                                non_matching_capacity_validation_points.append(
                                    {"CHWT": chwt, "ECWT": ecwt}
                                )

                non_matching_power_validation_points = []
                missing_power_validation_points = []
                for chwt in expected_chwt_temps:
                    for ecwt in expected_ecwt_temps:
                        dict_key = f"{chwt}, {ecwt}"
                        if power_validation_pts_dict.get(dict_key):
                            given_plrs = []
                            for power_validation_point in power_validation_pts_dict[
                                dict_key
                            ]:
                                load = power_validation_point.get(
                                    "load", 0.0 * ureg("W")
                                )
                                given_power = power_validation_point.get("result")
                                plr = load / given_capacities[dict_key]

                                if plr in expected_validation_plr:
                                    given_plrs.append(plr)
                                    eir_plr = (
                                        plr_coefficients[0]
                                        + plr_coefficients[1] * plr
                                        + plr_coefficients[2] * plr**2
                                    )
                                    eir_ft = (
                                        eir_f_t_coefficients[0]
                                        + eir_f_t_coefficients[1] * chwt
                                        + eir_f_t_coefficients[2] * chwt**2
                                        + eir_f_t_coefficients[3] * ecwt
                                        + eir_f_t_coefficients[4] * ecwt**2
                                        + eir_f_t_coefficients[5] * chwt * ecwt
                                    )

                                    expected_power = (
                                        given_capacity[dict_key]
                                        * eir_ft
                                        * eir_plr
                                        * rated_power
                                        / rated_capacity_b
                                    )

                                    if expected_power == given_power:
                                        missing_power_validation_points.append(
                                            {"CHWT": chwt, "ECWT": ecwt, "PLR": "ALL"}
                                        )
                                    else:
                                        missing_power_validation_points.append(
                                            {"CHWT": chwt, "ECWT": ecwt, "PLR": plr}
                                        )

                return {
                    "non_matching_power_validation_points_len": len(
                        non_matching_power_validation_points
                    ),
                    "missing_capacity_validation_points_len": len(
                        missing_capacity_validation_points
                    ),
                    "non_matching_capacity_validation_points_len": len(
                        non_matching_capacity_validation_points
                    ),
                    "missing_power_validation_points_len": len(
                        missing_power_validation_points
                    ),
                }
            else:
                return {
                    "non_matching_power_validation_points_len": None,
                    "missing_capacity_validation_points_len": None,
                    "non_matching_capacity_validation_points_len": None,
                    "missing_power_validation_points_len": None,
                }

        def rule_check(self, context, calc_vals=None, data=None):
            non_matching_power_validation_points_len = calc_vals[
                "non_matching_power_validation_points_len"
            ]
            missing_capacity_validation_points_len = calc_vals[
                "missing_capacity_validation_points_len"
            ]
            non_matching_capacity_validation_points_len = calc_vals[
                "non_matching_capacity_validation_points_len"
            ]
            missing_power_validation_points_len = calc_vals[
                "missing_power_validation_points_len"
            ]

            return (
                non_matching_power_validation_points_len
                == missing_capacity_validation_points_len
                == non_matching_capacity_validation_points_len
                == missing_power_validation_points_len
                == 0
            )
