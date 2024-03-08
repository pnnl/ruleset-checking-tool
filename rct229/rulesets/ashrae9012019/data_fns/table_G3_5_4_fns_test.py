from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_4_fns import table_G3_5_4_lookup


# Testing table_3_5_4------------------------------------------
def test__table_3_5_4_ptac():
    assert table_G3_5_4_lookup("PTAC (cooling mode)") == {
        "minimum_efficiency_copnf": 3.2
    }


def test__table_3_5_4_pthp_cooling():
    assert table_G3_5_4_lookup("PTHP (cooling mode)") == {
        "minimum_efficiency_copnf": 3.1
    }


def test__table_3_5_4_pthp_heating():
    assert table_G3_5_4_lookup("PTHP (heating mode)") == {
        "minimum_efficiency_copnf": 3.1
    }
