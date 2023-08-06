import typing
from famegui import models


class SchemaAgentType:
    """ Represents a schema agent type """

    def __init__(self, name: str):
        assert name != ""
        self._name = name
        self._attributes = {}
        self._products = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def attributes(self) -> typing.Dict[str, models.SchemaAttribute]:
        return self._attributes

    def add_attribute(self, attr: models.SchemaAttribute):
        if attr.name in self._attributes:
            raise ValueError("can't add attribute '{}' to agent type '{}' because it already exists".format(
                attr.name, self.name))
        self._attributes[attr.name] = attr

    @property
    def products(self) -> typing.List[str]:
        return self._products

    def set_products(self, products: typing.List[str]):
        self._products = products
