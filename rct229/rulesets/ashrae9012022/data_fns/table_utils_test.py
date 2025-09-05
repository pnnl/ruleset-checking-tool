from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry

FAKE_OSSTD_TABLE = {
    "fake_list": [
        {
            "match_field": 1,
            "other_field": "some_value",
        },
        {
            "match_field": 2,
            "other_field": "some_other_value",
        },
    ]
}


def test__find_osstd_table_entry__with_single_pair():
    assert find_osstd_table_entry(
        [("match_field", 2)],
        osstd_table=FAKE_OSSTD_TABLE,
    ) == {
        "match_field": 2,
        "other_field": "some_other_value",
    }
