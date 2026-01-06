from rct229.rulesets.ashrae9012022.data_fns.table_J_4_fns import table_J_4_lookup


def test__table_J_4_A_EIR_f_T():
    assert table_J_4_lookup("A", "EIR-f-T") == [
        1.777758,
        -0.038258,
        0.000431,
        -0.005368,
        0.000118,
        -0.000115,
    ]


def test__table_J_4_B_CAP_f_T():
    assert table_J_4_lookup("B", "CAP-f-T") == [
        -1.153535,
        0.075066,
        -0.000622,
        0.009777,
        -0.000071,
        -0.000057,
    ]


def test__table_J_4_C_EIR_f_PLR():
    assert table_J_4_lookup("C", "EIR-f-PLR") == [0.243730, 0.165972, 0.586099]


def test__table_J_4_M_EIR_f_T():
    assert table_J_4_lookup("M", "EIR-f-T") == [
        2.018167,
        -0.045111,
        0.000485,
        -0.008503,
        0.000168,
        -0.000124,
    ]


def test__table_J_4_N_CAP_f_T():
    assert table_J_4_lookup("N", "CAP-f-T") == [
        -0.840342,
        0.071938,
        -0.000641,
        0.002703,
        -0.000047,
        0.000007,
    ]


def test__table_J_4_S_EIR_f_PLR():
    assert table_J_4_lookup("S", "EIR-f-PLR") == [0.064979, 0.151829, 0.779131]
