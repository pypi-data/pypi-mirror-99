import typing
import os

from famegui import models


class Schema:
    """ Represents a schema to be applied on a scenario """

    def __init__(self, file_path: str):
        assert os.path.isabs(file_path)
        self._file_path = file_path
        self._agent_types = {}

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def agent_types(self) -> typing.Dict[str, models.SchemaAgentType]:
        return self._agent_types

    def add_agent_type(self, agent_type: models.SchemaAgentType):
        self._agent_types[agent_type.name] = agent_type

    def agent_type_from_name(self, name: str) -> models.SchemaAgentType:
        return self._agent_types[name] if name in self._agent_types else None
