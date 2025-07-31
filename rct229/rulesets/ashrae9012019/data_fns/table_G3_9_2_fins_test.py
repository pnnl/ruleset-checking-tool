from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_2_fins import table_G3_9_2_lookup


def test__table_G3_9_lookup__4_story_building():
    assert table_G3_9_2_lookup(
        number_of_stories=4,
    ) == {"mechanical_efficiency": 0.58, "motor_type": "Hydraulic"}


def test__table_G3_9_lookup__6_story_building():
    assert table_G3_9_2_lookup(
        number_of_stories=6,
    ) == {"mechanical_efficiency": 0.64, "motor_type": "Traction"}
