from jsonpath_ng import parse

def find_all(jpath, obj):
    return [match.value for match in parse(jpath).find(obj)]
