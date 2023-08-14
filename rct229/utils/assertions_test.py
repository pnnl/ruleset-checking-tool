from rct229.utils.assertions import MissingKeyException, get_first_attr_, getattr_

GETATTR_TEST_OBJ = {"field1": {"id": "f1", "field2": {"id": "f1", "field3": 7}}}
GETFIRSTATTR_TEST_OBJ = {"id": "c1", "u_factor": 1.234}


# Testing getattr_
def test__getattr___with_required_fields():
    assert getattr_(GETATTR_TEST_OBJ, "Obj", "field1", "field2", "field3") == 7


def test__getattr___with_missing_field():
    try:
        getattr_(GETATTR_TEST_OBJ, "Obj", "field1", "field2", "field4")
    except MissingKeyException as e:
        assert str(e) == "field2:f1 is missing field4"


def test__get_first_attr__with_required_fields():
    assert (
        get_first_attr_(
            GETFIRSTATTR_TEST_OBJ, "construction", ["u_factor", "c_factor", "f_factor"]
        )
        == 1.234
    )


def test__get_first_attr__with_missing_fields():
    try:
        get_first_attr_(GETFIRSTATTR_TEST_OBJ, "construction", ["c_factor", "f_factor"])
    except MissingKeyException as e:
        assert (
            str(e)
            == "construction:c1 is missing one of the fields in: ['c_factor', 'f_factor']"
        )
