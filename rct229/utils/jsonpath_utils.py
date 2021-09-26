from jsonpath_ng.ext import parse


def find_all(jpath, obj):
    return [match.value for match in parse(jpath).find(obj)]
