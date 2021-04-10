import pytest

from ruletest_engine import generate_test_rmrs

test_dict__no_template = {
    "rmr_transformations": {
        "user": {
            "transformers": [
                { "name": "Transformer_1" },
                { "name": "Transformer_2" }
            ]
        },
        "baseline": {
            "transformers": [
                { "name": "Transformer_1" }
            ]
        }
    }
}

test_dict__with_template = {
    "rmr_template": {
        "transformers": [
            { "name": "Transformer_1" },
            { "name": "Transformer_2" }
        ]
    },
    "rmr_transformations": {
        "user": {
            # To overwrite the transformer at index 1 of rmr_template
            "transformers/1": { "name": "Transformer_a" }
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
                { "name": "Transformer_1" },
                { "name": "Transformer_a" }
            ]
        },
        None,
        {
            "transformers": [
                { "name": "Transformer_1" },
                { "name": "Transformer_2" }
            ]
        }
    )

def test__generate_test_rmrs__no_template():
    assert generate_test_rmrs(test_dict__no_template) == (
        {
            "transformers": [
                {
                    "name": "Transformer_1"
                },
                {
                    "name": "Transformer_2"
                }
            ]
        },
        {
            "transformers": [
                {
                    "name": "Transformer_1"
                }
            ]
        },
        None
    )
