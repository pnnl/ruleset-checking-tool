from jsonpath_ng.ext import parse

# NOTE: jsonpath_ng.ext is used to get support for filtering
# and other extensions


def find_all(jpath, obj):
    return [match.value for match in parse(jpath).find(obj)]


def find_one(jpath, obj):
    matches = find_all(jpath, obj)

    return matches[0] if len(matches) > 0 else None


def find_exactly_one(jpath, obj):
    matches = find_all(jpath, obj)
    assert len(matches) == 1

    return matches[0]
