from jsonpath_ng import parse


def find_all(jpath, obj):
    return [match.value for match in parse(jpath).find(obj)]


def find_one(jpath, obj):
    matches = final_all(jpath, obj)

    return matches[0] if len(matches) > 0 else None


def find_exactly_one(jpath, obj):
    matches = final_all(jpath, obj)
    assert len(matches) == 1

    return matches[0]
