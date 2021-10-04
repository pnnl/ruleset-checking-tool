from jsonpath_ng.ext import parse
# NOTE: jsonpath_ng.ext is used to get support for filtering
# and other extensions


def find_all(jpath, obj):
    return [match.value for match in parse(jpath).find(obj)]
