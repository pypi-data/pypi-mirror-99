import typing

from famegui import models


class Scenario:
    def __init__(self):
        self._props = models.ScenarioProperties()
        self._agents = {}
        self._contracts = []
        self._schema_path = ""

    @property
    def properties(self) -> models.ScenarioProperties:
        return self._props

    def set_properties(self, props: models.ScenarioProperties):
        if props.values != self._props.values:
            self._props = props
            return True
        return False

    @property
    def agents(self) -> typing.Dict[str, models.Agent]:
        return self._agents

    def agent(self, id) -> models.Agent:
        assert(id in self._agents)
        return self._agents[id]

    def add_agent(self, a):
        if a.id in self._agents:
            other_agent_type_name = self._agents[a.id].type_name
            raise ValueError("can't add agent type '{}' because its id '{}' is already used by agent '{}'".format(
                a.type_name, a.id, other_agent_type_name))
        self._agents[a.id] = a

    @property
    def contracts(self) -> typing.List[models.Contract]:
        """ Returns all the contracts as a list """
        return self._contracts

    def add_contract(self, c):
        if c.sender_id not in self._agents:
            raise ValueError(
                "can't add contract: invalid sender id '{}'".format(c.sender_id))
        if c.receiver_id not in self._agents:
            raise ValueError(
                "can't add contract: invalid receiver id '{}'".format(c.receiver_id))

        self._contracts.append(c)
        self._agents[c.sender_id].add_output(c.receiver_id)
        self._agents[c.receiver_id].add_input(c.sender_id)

    @property
    def schema_path(self) -> str:
        return self._schema_path

    def set_schema_path(self, schema_path: str):
        self._schema_path = schema_path
