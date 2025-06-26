from asec.fairness import ProtectedAttributes


def test_protected_attributes_single_attribute():
    """Test ProtectedAttributes with a single protected attribute."""
    config = ProtectedAttributes(privileged_classes={"gender": "male"})

    assert config.attribute_names == "gender"
    assert config.privileged_groups == "male"


def test_protected_attributes_multiple_attributes():
    """Test ProtectedAttributes with multiple protected attributes."""
    config = ProtectedAttributes(privileged_classes={"gender": "male", "race": "white"})

    assert config.attribute_names == ["gender", "race"]
    assert config.privileged_groups == ("male", "white")


def test_protected_attributes_empty_dict():
    """Test ProtectedAttributes with empty privileged_classes."""
    config = ProtectedAttributes(privileged_classes={})

    assert config.attribute_names == []
    assert config.privileged_groups == ()
