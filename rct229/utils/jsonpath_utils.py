from jsonpath2.path import Path


def ensure_root(jpath):
    return jpath if jpath.startswith("$") else "$." + jpath


def find_all(jpath, obj):
    p = Path.parse_str(ensure_root(jpath))
    return [m.current_value for m in p.match(obj)]


def find_all_with_field_value(jpath, field, value, obj):
    p = Path.parse_str(ensure_root(f'{jpath}[?(@.{field}="{value}")]'))
    return [m.current_value for m in p.match(obj)]


def find_one(jpath, obj):
    matches = find_all(jpath, obj)

    return matches[0] if len(matches) > 0 else None


def find_one_with_field_value(jpath, field, value, obj):
    matches = find_all_with_field_value(jpath, field, value, obj)

    return matches[0] if len(matches) > 0 else None


def find_exactly_one_with_field_value(jpath, field, value, obj):
    matches = find_all_with_field_value(jpath, field, value, obj)
    assert (
        len(matches) == 1
    ), f"Search data referenced in {jpath} with key:value {field}:{value} returned {len(matches)} results instead of one"
    return matches[0]


def find_exactly_one(jpath, obj):
    matches = find_all(jpath, obj)
    assert (
        len(matches) == 1
    ), f"Search data referenced in {jpath} returned multiple or None results"
    return matches[0]
