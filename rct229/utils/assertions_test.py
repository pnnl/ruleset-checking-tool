from rct229.utils.assertions import getattr_

GETATTR_TEST_OBJ = {"field1": {"id": "f1", "field2": {"id": "f1", "field3": 7}}}

# Testing getattr_
def test__getattr___with_required_fields():
    assert getattr_(GETATTR_TEST_OBJ, "Obj", "field1", "field2", "field3") == 7

    def test__getattr___with_missing_field():
        with pytest.raises(AssertionError) as ae:
            getattr_(GETATTR_TEST_OBJ, "Obj", "field1", "field2", "field4")
        assert str(ae.value) == "Obj is missing field4 field"
