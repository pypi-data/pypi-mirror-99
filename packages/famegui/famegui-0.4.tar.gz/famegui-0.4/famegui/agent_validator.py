import logging
import typing
import os

from famegui import models
from famegui.appworkingdir import AppWorkingDir


class AgentValidator():
    def __init__(self, schema: models.Schema, working_dir: AppWorkingDir):
        self._schema = schema
        self._working_dir = working_dir

    def validate_agent(self, agent_model: models.Agent) -> typing.Tuple[bool, str]:
        logging.debug("validating agent {} of type '{}' with schema file '{}'".format(
            agent_model.id_str, agent_model.type_name, self._schema.file_path))

        agent_type = self._schema.agent_type_from_name(agent_model.type_name)
        if agent_type is None:
            return False, "invalid agent {}: agent type '{}' is not defined in schema '{}'".format(
                agent_model.id_str, agent_model.type_name, self._schema.file_path)

        # validate the existing attributes
        for attr_name, attr_value in agent_model.attributes.items():
            attr_full_name = "{}.{}".format(agent_model.type_name, attr_name)
            if not attr_name in agent_type.attributes:
                return False, "invalid agent {}: attribute '{}' is not defined in schema '{}'".format(
                    agent_model.id_str, attr_full_name, self._schema.file_path)
            else:
                attr = agent_type.attributes[attr_name]
                if not attr.is_compatible_value(attr_value):
                    return False, "invalid agent {}: value '{}' of attribute '{}' is rejected in schema '{}'".format(
                        agent_model.id_str, attr_value, attr_full_name, self._schema.file_path)
                if attr.type == models.AttributeType.TIME_SERIES:
                    # validate timeseries file path
                    file_path = self._working_dir.find_existing_child_file(
                        attr_value)
                    if file_path is None:
                        return False, "invalid agent {}: time series file '{}' not found in FAME working directory '{}'".format(
                            agent_model.id_str, attr_value, self._working_dir.root_dir)

        # find missing attributes
        for attr in agent_type.attributes.values():
            if attr.name not in agent_model.attributes:
                if attr.is_mandatory:
                    return False, "invalid agent {}: mandatory attribute '{}' is not defined".format(
                        agent_model.id_str, attr.name)

        return True, ""
