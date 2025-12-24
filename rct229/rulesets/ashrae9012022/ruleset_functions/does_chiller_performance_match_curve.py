from rct229.rulesets.ashrae9012022.data_fns.table_J_4_fns import table_J_4_lookup
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


class J4_CURVE:
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"


class J6_CURVE:
    V = "V"
    X = "X"
    Y = "Y"
    Z = "Z"
    AA = "AA"
    AB = "AB"


J4_CURVE_SET = [
    J4_CURVE.A,
    J4_CURVE.B,
    J4_CURVE.C,
    J4_CURVE.D,
    J4_CURVE.E,
    J4_CURVE.F,
    J4_CURVE.G,
    J4_CURVE.H,
    J4_CURVE.I,
    J4_CURVE.J,
    J4_CURVE.K,
    J4_CURVE.L,
    J4_CURVE.M,
    J4_CURVE.N,
    J4_CURVE.O,
    J4_CURVE.P,
    J4_CURVE.Q,
    J4_CURVE.R,
    J4_CURVE.S,
    J4_CURVE.T,
    J4_CURVE.U,
]
J6_CURVE_SET = [
    J6_CURVE.V,
    J6_CURVE.X,
    J6_CURVE.Y,
    J6_CURVE.Z,
    J6_CURVE.AA,
    J6_CURVE.AB,
]


def does_chiller_performance_match_curve(chiller: dict, curve_set: str) -> bool:
    """
    Evaluates whether the chiller performance curves align with the sets of performance curves specified in Appendix J of ASHRAE 90.1-2022 Appendix G.

    Parameters
    ----------
    chiller: dict
         The chiller object containing all relevant data for the chiller to be validated against the performance curves in Appendix J of ASHRAE 90.1-2022.
         This includes the rated capacity, full load efficiency (COP), compressor type, and the lists of capacity and power operating points.
    curve_set: str
        The curve set that the chiller is expected to align with. This should be a letter code of A, B, etc. to lookup in either Table J-4 or J-6.

    Returns
    -------
    bool
        boolean value indicating whether the chiller performance validation passed or failed.

    """

    if curve_set in J4_CURVE_SET:
        table_lookup = "J-4"
    elif curve_set in J6_CURVE_SET:
        table_lookup = "J-6"
    else:
        raise ValueError(
            "Invalid curve set provided. Must be A-U for Table J-4 or V-AB for Table J-6."
        )

    rated_capacity = getattr_(chiller, "chillers", "rated_capacity")
    efficiency_metric_type = getattr_(chiller, "chillers", "efficiency_metric_types")
    assert_(
        "FULL_LOAD_EFFICIENCY_RATED" in efficiency_metric_type,
        "The `FULL_LOAD_EFFICIENCY_RATED` must exist in the `efficiency_metric_types`.",
    )
    # find where the "FULL_LOAD_EFFICIENCY_RATED" is located
    full_load_efficiency_rated_position = efficiency_metric_type.index(
        "FULL_LOAD_EFFICIENCY_RATED"
    )

    full_load_efficiency_rated = getattr_(
        chiller, "chillers", "efficiency_metric_values"
    )[full_load_efficiency_rated_position]

    assert_(
        rated_capacity > 0 * ureg("W"), "The `capacity` value must be greater than 0 W."
    )
    assert_(
        full_load_efficiency_rated > 0,
        "The `efficiency_metric_values` must be greater than 0.",
    )

    rated_power = rated_capacity / full_load_efficiency_rated

    if table_lookup == "J-4":
        eir_f_t_coefficients = table_J_4_lookup(curve_set, "EIR-f-T")
        cap_f_t_coefficients = table_J_4_lookup(curve_set, "CAP-f-T")
        plr_coefficients = table_J_4_lookup(curve_set, "EIR-f-PLR")
    else:
        eir_f_t_coefficients = table_J_6_lookup(curve_set, "EIR-f-T")
        cap_f_t_coefficients = table_J_6_lookup(curve_set, "CAP-f-T")
        plr_coefficients = table_J_6_lookup(curve_set, "EIR-f-PLR")

    capacity_operating_pts_dict = {}
    capacity_operating_points = getattr_(
        chiller, "chillers", "capacity_operating_points"
    )
    for capacity_operating_point in capacity_operating_points:
        chilled_water_supply_temp = getattr_(
            capacity_operating_point,
            "capacity_operating_points",
            "chilled_water_supply_temperature",
        ).to("degF")
        condenser_temp = getattr_(
            capacity_operating_point,
            "capacity_operating_points",
            "condenser_temperature",
        ).to("degF")

        dict_key = (
            f"{round(chilled_water_supply_temp.m, 1)}, {round(condenser_temp.m, 1)}"
        )
        capacity_operating_pts_dict[dict_key] = getattr_(
            capacity_operating_point,
            "capacity_operating_points",
            "capacity",
        )
        assert_(
            capacity_operating_pts_dict[dict_key] > 0,
            "The 'capacity' value must be greater than 0 W.",
        )

    power_operating_pts_dict = {}
    power_operating_points = getattr_(chiller, "chillers", "power_operating_points")
    for power_operating_point in power_operating_points:
        chilled_water_supply_temp = getattr_(
            power_operating_point,
            "power_operating_points",
            "chilled_water_supply_temperature",
        ).to("degF")
        condenser_temp = getattr_(
            power_operating_point,
            "power_operating_points",
            "condenser_temperature",
        ).to("degF")

        dict_key = (
            f"{round(chilled_water_supply_temp.m, 1)}, {round(condenser_temp.m, 1)}"
        )

        power_operating_pts_dict.setdefault(dict_key, [])
        power_operating_pts_dict[dict_key].append(power_operating_point)

    given_capacities = {}
    non_matching_capacity_operating_points = []
    missing_capacity_operating_points = []
    for chwt in EXPECTED_CHILLED_WATER_TEMPS:
        for ecwt in EXPECTED_ENTERING_CONDENSER_WATER_TEMPS:
            dict_key = f"{chwt}, {ecwt}"
            if dict_key in capacity_operating_pts_dict:
                expected_capacity = (
                    cap_f_t_coefficients[0]
                    + cap_f_t_coefficients[1] * chwt
                    + cap_f_t_coefficients[2] * chwt**2
                    + cap_f_t_coefficients[3] * ecwt
                    + cap_f_t_coefficients[4] * ecwt**2
                    + cap_f_t_coefficients[5] * chwt * ecwt
                ) * rated_capacity

                given_capacity = capacity_operating_pts_dict[dict_key]
                given_capacities[dict_key] = given_capacity

                if not std_equal_with_precision(
                    given_capacity, expected_capacity, 1 * ureg("ton")
                ):
                    non_matching_capacity_operating_points.append(
                        {"CHWT": chwt, "ECWT": ecwt}
                    )
            else:
                missing_capacity_operating_points.append({"CHWT": chwt, "ECWT": ecwt})

    non_matching_power_operating_points = []
    missing_power_operating_points = []
    for chwt in EXPECTED_CHILLED_WATER_TEMPS:
        for ecwt in EXPECTED_ENTERING_CONDENSER_WATER_TEMPS:
            dict_key = f"{chwt}, {ecwt}"
            if dict_key in power_operating_pts_dict:
                for power_operating_point in power_operating_pts_dict[dict_key]:
                    load = getattr_(
                        power_operating_point, "power_operating_points", "load"
                    )
                    given_power = getattr_(
                        power_operating_point, "power_operating_points", "power"
                    )

                    plr = (
                        load / given_capacities[dict_key]
                    )  # already checked `given_capacities[dict_key]` > 0.0

                    # plr.m because plr is a "dimensionless" unit
                    if any(
                        [
                            std_equal_with_precision(plr.m, expected_plr, 2)
                            for expected_plr in EXPECTED_VALIDATION_PLR
                        ]
                    ):
                        if len(plr_coefficients) == 3:
                            eir_plr = (
                                plr_coefficients[0]
                                + plr_coefficients[1] * plr
                                + plr_coefficients[2] * plr**2
                            )
                        elif len(plr_coefficients) == 4:
                            eir_plr = (
                                plr_coefficients[0]
                                + plr_coefficients[1] * plr
                                + plr_coefficients[2] * plr**2
                                + plr_coefficients[3] * plr**3
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
                            given_power, expected_power, 1 * ureg("ton")
                        ):
                            non_matching_power_operating_points.append(
                                {"CHWT": chwt, "ECWT": ecwt, "PLR": "ALL"}
                            )
                    else:
                        missing_power_operating_points.append(
                            {"CHWT": chwt, "ECWT": ecwt, "PLR": plr}
                        )
            else:
                missing_power_operating_points.append(
                    {"CHWT": chwt, "ECWT": ecwt, "PLR": plr}
                )

    return (
        len(non_matching_capacity_operating_points)
        == len(missing_capacity_operating_points)
        == len(non_matching_power_operating_points)
        == len(missing_power_operating_points)
        == 0
    )
