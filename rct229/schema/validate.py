import json
import jsonschema
import os

file_dir = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(file_dir, 'rmr_schema.json')


def validate_rmr(rmr_obj):
    """Validate an RMR against the schema and other high-level checks"""

    if rmr_obj is None:
        # TODO: Maybe it makes sense to write out a function that returns this generalized pass dictionary
        return {'passed': True, 'error': None}

    # Validate against the schema
    result = _schema_validate(SCHEMA_PATH, rmr_obj)

    if result['passed']:
        # Provide non-schema validation
        result = _non_schema_validation(rmr_obj)

    return result


def _schema_validate(schema_path, rmr_obj):
    """Validates an RMR against the schema"""
    with open(schema_path) as schema_file:
        schema_obj = json.load(schema_file)

        try:
            # Throws ValidationError on failure
            jsonschema.validate(rmr_obj, schema_obj)
            return {
                "passed": True,
                "error": None
            }
        except jsonschema.exceptions.ValidationError as err:
            return {
                "passed": False,
                "error": "schema invalid: " + err.message
            }


def _non_schema_validation(rmr_obj):
    """Provides non-schema validation for an RMR"""
    # TODO: Add check for unique names, etc.
    return {"passed": True, "error": None}
