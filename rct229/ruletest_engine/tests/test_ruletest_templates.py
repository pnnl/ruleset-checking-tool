from rct229.ruletest_engine.ruletest_engine import generate_test_rmds

test_dict__no_template = {
    "rmd_transformations": {
        "user": {
            "transformers": [
                {"id": 1, "name": "Transformer_1"},
                {"id": 2, "name": "Transformer_2"},
            ]
        },
        "baseline": {
            "transformers": [
                {"id": 1, "name": "Transformer_1"},
            ]
        },
    }
}


def test__generate_test_rmds__no_template():
    assert generate_test_rmds(test_dict__no_template) == (
        {
            "transformers": [
                {"id": 1, "name": "Transformer_1"},
                {"id": 2, "name": "Transformer_2"},
            ]
        },
        {
            "transformers": [
                {"id": 1, "name": "Transformer_1"},
            ]
        },
        None,
    )
