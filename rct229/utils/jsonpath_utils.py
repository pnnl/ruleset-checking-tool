from jsonpath_ng.ext import parse

# NOTE: jsonpath_ng.ext is used to get support for filtering
# and other extensions


def find_all(jpath, obj):
    return [match.value for match in parse(jpath).find(obj)]


def find_all_with_field_value(jpath, field, value, obj):
    return [
        match.value for match in parse(f'{jpath}[?(@.{field}="{value}")]').find(obj)
    ]


def find_one(jpath, obj):
    matches = find_all(jpath, obj)

    return matches[0] if len(matches) > 0 else None


def find_one_with_field_value(jpath, field, value, obj):
    matches = find_all_with_field_value(jpath, field, value, obj)

    return matches[0] if len(matches) > 0 else None


def find_exactly_one_with_field_value(jpath, field, value, obj):
    matches = find_all_with_field_value(jpath, field, value, obj)
    assert len(matches) == 1, f"Search data referenced in {jpath} with key {value} returned multiple or None results"

    return matches[0]


def find_exactly_one(jpath, obj):
    matches = find_all(jpath, obj)
    assert len(matches) == 1, f"Search data referenced in {jpath} returned multiple or None results"

    return matches[0]
