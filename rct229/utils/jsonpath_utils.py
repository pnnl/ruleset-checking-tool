from itertools import chain

from jsonpath2 import match

from rct229.utils.assertions import assert_, getattr_


def create_jsonpath_value_dict(jpath, obj):
    return {
        m.node.tojsonpath(): m.current_value for m in match(ensure_root(jpath), obj)
    }


def ensure_root(jpath):
    return jpath if jpath.startswith("$") else "$." + jpath


def find_all(jpath, obj):
    return [m.current_value for m in match(ensure_root(jpath), obj)]


def find_all_by_jsonpaths(jpaths: list, obj: dict) -> list:
    return list(chain.from_iterable([find_all(jpath, obj) for jpath in jpaths]))


def find_all_with_field_value(jpath, field, value, obj):
    return [
        m.current_value
        for m in match(ensure_root(f'{jpath}[?(@.{field}="{value}")]'), obj)
    ]


def find_exactly_required_fields(req_fields, obj):
    for jpath, fields in req_fields.items():
        for element in find_all(jpath, obj):
            for field in fields:
                getattr_(element, element.get("id"), field)


def find_one(jpath, obj, default=None):
    matches = find_all(jpath, obj)

    return matches[0] if len(matches) > 0 else default


def find_one_with_field_value(jpath, field, value, obj):
    matches = find_all_with_field_value(jpath, field, value, obj)

    return matches[0] if len(matches) > 0 else None


def find_exactly_one_with_field_value(jpath, field, value, obj):
    matches = find_all_with_field_value(jpath, field, value, obj)
    # do another search using upper case if no matches
    if not matches:
        matches = find_all_with_field_value(jpath, field, value.upper(), obj)

    assert_(
        len(matches) == 1,
        f"Search data referenced in {jpath} with key:value {field}:{value} returned {len(matches)} results instead of one",
    )
    return matches[0]


def find_exactly_one(jpath, obj):
    matches = find_all(jpath, obj)
    assert_(
        len(matches) == 1,
        f"Search data referenced in {jpath} returned multiple or None results",
    )
    return matches[0]


def find_ruleset_model_type(rmd):
    """
    Search for the ruleset model type from an RMD

    Parameters
    ----------
    rmd: json

    Returns: str
    -------

    """
    return find_exactly_one("$.type", rmd)


def convert_absolute_path_list_to_jsonpath(input_list):
    jsonpath = "$"  # Start with the root '$'
    for i, item in enumerate(input_list):
        if isinstance(item, str):
            jsonpath += f".{item}"  # Append strings as keys
        elif isinstance(item, int):
            jsonpath += f"[{item}]"  # Append integers as array indices

    return jsonpath


def format_jsonpath_with_id(input_list):
    if not input_list:
        return
    # Replace the last item in the list with 'id'
    input_list = input_list[:-1] + ["id"]
    return convert_absolute_path_list_to_jsonpath(input_list)
