from rct229.ruleset_functions.check_purchased_chw_hhw import check_purchased_chw_hhw

TEST_RMD = {}


def test_check_purchased_chw_hhw():
    assert check_purchased_chw_hhw(TEST_RMD) == {
        "purchased_cooling": False,
        "purchased_heating": False,
    }
