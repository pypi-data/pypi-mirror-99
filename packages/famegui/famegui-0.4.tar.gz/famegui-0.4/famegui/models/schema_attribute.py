import typing

from fameio.source.AttributeValidator import AttributeType, AttributeValidator


def _find_attr_type_by_name(name: str):
    name = name.upper()
    if name in AttributeType.__members__:
        return AttributeType.__members__[name]
    return None


class SchemaAttribute:
    """ Details about an agent attribute as defined by a schema """

    def __init__(self, attr_name: str, type_name: str, is_mandatory: bool, enum_values: typing.List[str] = None):
        attr_type = _find_attr_type_by_name(type_name)
        if attr_type is None:
            raise ValueError("invalid attribute type '{}'".format(attr_type))

        if attr_type == AttributeType.ENUM:
            if enum_values is None or len(enum_values) == 0:
                raise ValueError(
                    "enum values are missing for attribute '{}'".format(attr_name))
            else:
                for v in enum_values:
                    assert v != ""
        elif enum_values is not None:
            raise ValueError(
                "enum values can't be specified for attribute '{}' of type '{}'".format(attr_name, attr_type))

        self._attr_name = attr_name
        self._attr_type = attr_type
        self._is_mandatory = is_mandatory
        self._enum_values = enum_values

    @property
    def name(self) -> str:
        return self._attr_name

    @property
    def type(self) -> AttributeType:
        return self._attr_type

    @property
    def type_name(self) -> str:
        return self._attr_type.name.lower()

    @property
    def is_mandatory(self) -> bool:
        return self._is_mandatory

    @property
    def enum_values(self) -> typing.List[str]:
        return self._enum_values

    def is_compatible_value(self, value) -> bool:
        if self.type.is_compatible(value):
            if self.type == AttributeType.ENUM:
                return value in self.enum_values
            return True
        return False
