from rct229.rulesets.ashrae9012022.data_fns.table_J_6_fns import table_J_6_lookup


def test__table_J_6_X_EIR_f_T():
    assert table_J_6_lookup("X", "EIR-f-T") == [
        1.037805,
        -0.024695,
        0.000329,
        0.00313,
        0.000102,
        -0.000159,
    ]


def test__table_J_6_Y_CAP_f_T():
    assert table_J_6_lookup("Y", "CAP-f-T") == [
        -0.160681,
        0.04439,
        -0.000429,
        0.001024,
        -0.000035,
        0.000055,
    ]


def test__table_J_6_AA_EIR_f_PLR():
    assert table_J_6_lookup("AA", "EIR-f-PLR") == [0.339494, 0.04909, 0.611582]
