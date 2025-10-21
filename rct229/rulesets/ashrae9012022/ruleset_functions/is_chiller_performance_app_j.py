from rct229.rulesets.ashrae9012022.data_fns.table_J_6_fns import table_J_6_lookup
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.std_comparisons import std_equal_with_precision

ENERGY_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]
CHILLER_COMPRESSOR = SchemaEnums.schema_enums["ChillerCompressorOptions"]
CHILLER_EFFICIENCY_METRIC = SchemaEnums.schema_enums["ChillerEfficiencyMetricOptions"]


EXPECTED_VALIDATION_PLR = [0.25, 0.50, 0.75, 1.00]
EXPECTED_CHILLED_WATER_TEMPS = [39.0, 45.0, 50.0, 55.0]
EXPECTED_ENTERING_CONDENSER_WATER_TEMPS = [60.0, 72.5, 85.0, 97.5, 104.0]


def is_chiller_performance_app_j(chiller: dict) -> bool:
    """
    Evaluates whether the chiller performance curves align with the sets of performance curves specified in Appendix J of ASHRAE 90.1-2022 Appendix G.

    Parameters
    ----------
    chiller: dict
         The chiller object containing all relevant data for the chiller to be validated against the performance curves in Appendix J of ASHRAE 90.1-2022.
         This includes the rated capacity, full load efficiency (COP), compressor type, and the lists of capacity and power validation points.

    Returns
    -------
    bool
        boolean value indicating whether the chiller performance validation passed or failed.

    """

    compressor_type = getattr_(chiller, "chillers", "compressor_type")
    rated_capacity = getattr_(chiller, "chillers", "rated_capacity")
    if compressor_type == CHILLER_COMPRESSOR.CENTRIFUGAL:
        if rated_capacity < 150 * ureg("ton"):
            curve_set = "Z"
        elif 150 * ureg("ton") <= rated_capacity < 300 * ureg("ton"):
            curve_set = "AA"
        else:
            curve_set = "AB"
    elif compressor_type in (
        CHILLER_COMPRESSOR.POSITIVE_DISPLACEMENT,
        CHILLER_COMPRESSOR.SCROLL,
        CHILLER_COMPRESSOR.SCREW,
    ):
        if rated_capacity < 150 * ureg("ton"):
            curve_set = "V"
        elif rated_capacity > 300 * ureg("ton"):
            curve_set = "Y"
        else:
            curve_set = "X"
    else:
        curve_set = None

    if curve_set is not None:
        # The first element is "FULL_LOAD_EFFICIENCY_RATED"
        full_load_efficiency_rated = getattr_(
            chiller, "chillers", "efficiency_metric_values"
        )[0]
        assert_(
            full_load_efficiency_rated > 0,
            "The `full_load_efficiency_rated` value must be greater than 0.",
        )

        rated_power = rated_capacity / full_load_efficiency_rated

        eir_f_t_coefficients = table_J_6_lookup(curve_set, "EIR-f-T")
        cap_f_t_coefficients = table_J_6_lookup(curve_set, "CAP-f-T")
        plr_coefficients = table_J_6_lookup(curve_set, "EIR-f-PLR")

        capacity_validation_pts_dict = {}
        capacity_operating_points = getattr_(
            chiller, "chillers", "capacity_operating_points"
        )
        for capacity_validation_point in capacity_operating_points:
            chilled_water_supply_temp = getattr_(
                capacity_validation_point,
                "capacity_operating_points",
                "chilled_water_supply_temperature",
            ).to("degF")
            condenser_temp = getattr_(
                capacity_validation_point,
                "capacity_operating_points",
                "condenser_temperature",
            ).to("degF")

            dict_key = (
                f"{round(chilled_water_supply_temp.m, 1)}, {round(condenser_temp.m, 1)}"
            )
            capacity_validation_pts_dict[dict_key] = getattr_(
                capacity_validation_point,
                "capacity_operating_points",
                "capacity",
            )
            assert_(
                capacity_validation_pts_dict[dict_key] > 0,
                "The 'capacity' value must be greater than 0 W.",
            )

        power_validation_pts_dict = {}
        power_operating_points = getattr_(chiller, "chillers", "power_operating_points")
        for power_validation_point in power_operating_points:
            chilled_water_supply_temp = getattr_(
                power_validation_point,
                "power_operating_points",
                "chilled_water_supply_temperature",
            ).to("degF")
            condenser_temp = getattr_(
                power_validation_point,
                "power_operating_points",
                "condenser_temperature",
            ).to("degF")

            dict_key = (
                f"{round(chilled_water_supply_temp.m, 1)}, {round(condenser_temp.m, 1)}"
            )

            power_validation_pts_dict.setdefault(dict_key, [])
            power_validation_pts_dict[dict_key].append(power_validation_point)

        given_capacities = {}
        missing_capacity_validation_points = []
        non_matching_capacity_validation_points = []
        for chwt in EXPECTED_CHILLED_WATER_TEMPS:
            for ecwt in EXPECTED_ENTERING_CONDENSER_WATER_TEMPS:
                dict_key = f"{chwt}, {ecwt}"
                if capacity_validation_pts_dict.get(dict_key):
                    expected_capacity = (
                        cap_f_t_coefficients[0]
                        + cap_f_t_coefficients[1] * chwt
                        + cap_f_t_coefficients[2] * chwt**2
                        + cap_f_t_coefficients[3] * ecwt
                        + cap_f_t_coefficients[4] * ecwt**2
                        + cap_f_t_coefficients[5] * chwt * ecwt
                    ) * rated_capacity

                    given_capacity = capacity_validation_pts_dict[dict_key]
                    given_capacities[dict_key] = given_capacity

                    if not std_equal_with_precision(
                        given_capacity, expected_capacity, 1 * ureg("W")
                    ):
                        non_matching_capacity_validation_points.append(
                            {"CHWT": chwt, "ECWT": ecwt}
                        )
                else:
                    missing_capacity_validation_points.append(
                        {"CHWT": chwt, "ECWT": ecwt}
                    )

        non_matching_power_validation_points = []
        missing_power_validation_points = []
        for chwt in EXPECTED_CHILLED_WATER_TEMPS:
            for ecwt in EXPECTED_ENTERING_CONDENSER_WATER_TEMPS:
                dict_key = f"{chwt}, {ecwt}"
                if power_validation_pts_dict.get(dict_key):
                    for power_validation_point in power_validation_pts_dict[dict_key]:
                        load = getattr_(
                            power_validation_point, "power_operating_points", "load"
                        )
                        given_power = getattr_(
                            power_validation_point, "power_operating_points", "power"
                        )

                        plr = (
                            load / given_capacities[dict_key]
                        )  # no need to check `given_capacities[dict_key]` = 0.0 (checked in line 95)

                        # plr.m because plr is a "dimensionless" unit
                        if any(
                            [
                                std_equal_with_precision(plr.m, expected_plr, 2)
                                for expected_plr in EXPECTED_VALIDATION_PLR
                            ]
                        ):
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
                                given_capacities[dict_key]
                                * eir_ft
                                * eir_plr
                                * rated_power
                                / rated_capacity
                            )

                            if not std_equal_with_precision(
                                given_power, expected_power, 1 * ureg("W")
                            ):
                                non_matching_power_validation_points.append(
                                    {"CHWT": chwt, "ECWT": ecwt, "PLR": "ALL"}
                                )
                        else:
                            missing_power_validation_points.append(
                                {"CHWT": chwt, "ECWT": ecwt, "PLR": plr}
                            )
                else:
                    missing_power_validation_points.append(
                        {"CHWT": chwt, "ECWT": ecwt, "PLR": plr}
                    )

    return (
        len(non_matching_capacity_validation_points)
        == len(missing_capacity_validation_points)
        == len(non_matching_power_validation_points)
        == len(missing_power_validation_points)
        == 0
    )
