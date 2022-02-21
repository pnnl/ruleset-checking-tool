from rct229.utils.jsonpath_utils import find_all


def assert_(bool, err_msg):
    assert bool, err_msg


def assert_nonempty_lists(req_nonempty_lists, obj):
    for jpath in req_nonempty_lists:
        for req_list in find_all(jpath + "[*]", obj):
            assert len(req_list) > 0, f"{jpath} id:{req_list['id']} is empty"


def assert_required_fields(req_fields, obj):
    for (jpath, fields) in req_fields.items():
        for element in find_all(jpath, obj):
            for field in fields:
                assert (
                    field in element
                ), f"Missing {field} in {jpath} id:{element.get('id')}"


def getattr_(obj, key, err_msg):
    assert key in obj, err_msg
    return obj[key]
