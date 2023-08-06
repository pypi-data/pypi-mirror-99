import logging
import typing
from PySide2 import QtCore

from famegui import models
from famegui.agent_controller import AgentController
from famegui.appworkingdir import AppWorkingDir
from famegui.agent_validator import AgentValidator


class ProjectProperties(QtCore.QObject):
    """ Class used to attach extra properties to a scenario model and signal when they change """

    changed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self, schema: models.Schema = None, file_path=""):
        self._has_unsaved_changes = False
        self._file_path = file_path
        self._schema = schema
        self._validation_errors = []
        self.changed.emit()

    @property
    def is_open(self) -> bool:
        return self._schema is not None

    @property
    def has_unsaved_changes(self) -> bool:
        return self._has_unsaved_changes

    def set_unsaved_changes(self, has_changes: bool):
        assert self.is_open
        if self._has_unsaved_changes != has_changes:
            self._has_unsaved_changes = has_changes
            self.changed.emit()

    @property
    def file_path(self) -> str:
        return self._file_path

    def set_file_path(self, file_path: str):
        assert self.is_open
        if self._file_path != file_path:
            self._file_path = file_path
            self.changed.emit()

    @property
    def schema(self) -> models.Schema:
        assert self._schema is not None
        return self._schema

    @property
    def schema_path(self) -> str:
        return self.schema.file_path

    @property
    def is_validation_successful(self) -> bool:
        #assert self.is_open
        return len(self._validation_errors) == 0

    @property
    def validation_errors(self) -> typing.List[str]:
        assert self.is_open
        return self._validation_errors

    def add_validation_error(self, msg: str):
        was_valid = self.is_validation_successful
        self._validation_errors.append(msg)
        if was_valid:
            logging.info(
                "schema validation status changed from successful to failed")
            self.changed.emit()


class MainController(QtCore.QObject):
    # agent selection update
    selected_agent_changed = QtCore.Signal(AgentController)
    # new agent added
    agent_added = QtCore.Signal(AgentController)
    # new contract added
    contract_added = QtCore.Signal(
        AgentController, AgentController, models.Contract)  # sender, receiver, contract

    def __init__(self, working_dir: AppWorkingDir):
        super().__init__()
        logging.debug("initializing main controller")
        self._working_dir = working_dir
        self._scenario_model = None
        self._agents = {}
        self._contracts = {}
        self._project_properties = ProjectProperties()

    def reset(self):
        self._agents = {}
        self._contracts = {}
        self._project_properties.reset()
        self._scenario_model = None

    @property
    def is_open(self) -> bool:
        return self._scenario_model is not None and self.project_properties.is_open

    @property
    def has_unsaved_changes(self) -> bool:
        return self.project_properties.has_unsaved_changes

    @property
    def project_properties(self) -> ProjectProperties:
        return self._project_properties

    @property
    def schema(self) -> models.Schema:
        return self._project_properties.schema

    @property
    def scenario(self) -> models.Scenario:
        return self._scenario_model

    def set_scenario_properties(self, props: models.Scenario):
        has_changed = self._scenario_model.set_properties(props)
        if has_changed:
            self._project_properties.set_unsaved_changes(True)

    @property
    def can_export_protobuf(self) -> bool:
        return self.is_open and self.project_properties.is_validation_successful and self.has_unsaved_changes == False

    @property
    def agent_count(self) -> int:
        return len(self._agents)

    @property
    def agent_list(self) -> typing.List[AgentController]:
        assert self.is_open
        return self._agents.values()

    def agent_from_id(self, id: int) -> AgentController:
        assert id in self._agents
        return self._agents[id]

    @property
    def contract_count(self) -> int:
        return len(self._contracts)

    def generate_new_agent_id(self):
        new_id = len(self._agents) + 1
        # note: we don't control how ids have been generated for agents created from an external source
        # so we check for possible conflict and solve it
        if new_id in self._agents:
            for i in range(1, len(self._agents) + 2):
                if not i in self._agents:
                    new_id = i
                    break
        logging.debug("generated new agent id {}".format(new_id))
        return new_id

    # the given agent id can be 0 to clear the current selection
    def set_selected_agent_id(self, agent_id: int):
        assert self.is_open
        if agent_id not in self._agents:
            assert agent_id == 0 or agent_id is None
            self.selected_agent_changed.emit(None)
        else:
            self.selected_agent_changed.emit(self._agents[agent_id])

    def add_new_agent(self, agent_model: models.Agent, x: int, y: int):
        assert self.is_open
        agent_model.set_display_xy(x, y)
        self._validate_and_create_agent_controller(agent_model)
        self._scenario_model.add_agent(agent_model)
        self._project_properties.set_unsaved_changes(True)
        logging.info("created new agent {} of type '{}'".format(
            agent_model.id_str, agent_model.type_name))

    def _validate_and_create_agent_controller(self, agent_model: models.Agent):
        assert self.is_open

        # accept to add the agent even if invalid
        agent = AgentController(agent_model)
        self._agents[agent.id] = agent

        # perform schema validation
        validator = AgentValidator(self.schema, self._working_dir)
        ok, err_msg = validator.validate_agent(agent_model)
        if not ok:
            logging.warning(err_msg)
            self._project_properties.add_validation_error(err_msg)

        logging.info("new agent {} added".format(agent_model.id_str))
        self.agent_added.emit(agent)

    def add_new_contract(self, contract_model: models.Contract):
        self._scenario_model.add_contract(contract_model)
        self._create_contract_model(contract_model)
        self._project_properties.set_unsaved_changes(True)
        logging.info("created new contract '{}' between {} and {}".format(
            contract_model.product_name, contract_model.sender_id_str, contract_model.receiver_id_str))

    def _create_contract_model(self, contract: models.Contract):
        assert self.is_open
        # should be enforced when creating / reading the contract
        assert contract.sender_id != contract.receiver_id

        # validate sender / receiver are known
        if contract.sender_id not in self._agents:
            raise ValueError("can't add contract '{}' because sender agent id '{}' is unknown".format(
                contract.name, contract.sender_id))
        if contract.receiver_id not in self._agents:
            raise ValueError("can't add contract '{}' because receiver agent id '{}' is unknown".format(
                contract.name, contract.receiver_id))

        sender_ctrl = self._agents[contract.sender_id]
        receiver_ctrl = self._agents[contract.receiver_id]

        # connect agents
        sender_ctrl.model.add_output(contract.receiver_id)
        receiver_ctrl.model.add_input(contract.sender_id)

        self.contract_added.emit(sender_ctrl, receiver_ctrl, contract)

    def create_new_scenario(self, schema: models.Schema):
        # don't call this function when a scenario already exists to avoid accidental loss of data
        assert not self.is_open

        self._scenario_model = models.Scenario()
        self._scenario_model.set_schema_path(schema.file_path)
        self._scenario_model.properties.init_missing_values()
        self._project_properties.reset(schema)
        self._project_properties.set_unsaved_changes(True)

    def open_scenario(self, scenario: models.Scenario, file_path: str, schema: models.Schema):
        logging.debug("opening new scenario and schema")
        self.reset()

        changed_done = False
        if scenario.schema_path != schema.file_path:
            scenario.set_schema_path(schema.file_path)
            changed_done = True

        try:
            self._scenario_model = scenario
            if self._scenario_model.properties.init_missing_values():
                logging.warning(
                    "the loaded scenario file was updated to contain all the required properties")
                changed_done = True

            self._project_properties.reset(schema, file_path)
            self._project_properties.set_unsaved_changes(changed_done)

            # process and validate the scenario
            for a in self._scenario_model.agents.values():
                self._validate_and_create_agent_controller(a)
            for c in self._scenario_model.contracts:
                self._create_contract_model(c)
        except:
            logging.warning(
                "failed to open the scenario with the given schema")
            self.reset()
            raise

        # refresh the UI
        self._project_properties.changed.emit()

    def save_to_file(self, file_path):
        assert self.is_open
        logging.info("saving scenario to file {}".format(file_path))
        models.ScenarioLoader.save_to_yaml_file(
            self._scenario_model, file_path)
        # update status
        self._project_properties.set_unsaved_changes(False)
        self._project_properties.set_file_path(file_path)
