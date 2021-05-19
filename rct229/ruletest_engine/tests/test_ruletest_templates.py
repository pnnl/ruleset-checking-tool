
from rct229.ruletest_engine.ruletest_engine import generate_test_rmrs

test_dict__no_template = {
    "rmr_transformations": {
        "user": {
            "transformers": [
                {"id": 1,
                 "name": "Transformer_1"},
                {"id": 2,
                 "name": "Transformer_2"},
            ]
        },
        "baseline": {
            "transformers": [
                {"id": 1,
                 "name": "Transformer_1"},
            ]
        }
    }
}

test_dict__with_template = {
    "rmr_template": {
        "user": True,
        "proposed": True,
        "json_template": {
            "transformers": [
                {"id": 1},
                {"id": 2}
            ]
        }

    },
    "rmr_transformations": {
        "user": {
            # To add ids to rmr_template
            "transformers": [
                {"name": "Transformer_1"},
                {"name": "Transformer_2"}
            ]
        },
        # Leave rmr_template unchanged
        "proposed": {}
        # Since baseline is not specified, it will be set to None
    }
}


def test__generate_test_rmrs__with_template():
    assert generate_test_rmrs(test_dict__with_template) == (
        {
            "transformers": [
                {"id": 1,
                 "name": "Transformer_1"},
                {"id": 2,
                 "name": "Transformer_2"},
            ]
        },
        None,
        {
            "transformers": [
                {"id": 1},
                {"id": 2}
            ]
        }
    )


def test__generate_test_rmrs__no_template():
    assert generate_test_rmrs(test_dict__no_template) == (
        {
            "transformers": [
                {"id": 1,
                 "name": "Transformer_1"},
                {"id": 2,
                 "name": "Transformer_2"},
            ]
        },
        {
            "transformers": [
                {"id": 1,
                 "name": "Transformer_1"},
            ]
        },
        None
    )
