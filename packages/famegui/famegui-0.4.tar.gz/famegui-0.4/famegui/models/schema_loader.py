import logging
import os

from famegui import models
import famegui.models.yaml_utils as yaml_utils


def _extract_attribute(attr_name, attr_items) -> models.SchemaAttribute:
    attr_type = yaml_utils.must_get_str_key(attr_items, "AttributeType")
    # optional fields
    is_mandatory = attr_items.get("Mandatory")
    enum_values = attr_items.get("Values")

    return models.SchemaAttribute(attr_name, attr_type, is_mandatory, enum_values)


def _extract_attributes(agent_type_name, items) -> models.SchemaAgentType:
    result = models.SchemaAgentType(agent_type_name)

    attributes = items.get("Attributes")
    if attributes is None:
        logging.info(
            "no attribute defined in schema for agent type '{}'".format(agent_type_name))
    else:
        for attr_name, attr_items in attributes.items():
            logging.debug("loading attribute '{}.{}'".format(
                agent_type_name, attr_name))
            result.add_attribute(_extract_attribute(attr_name, attr_items))

    # it's ok to not define any attribute, but at least one product must be defined
    # otherwise the agent type can't be connected to
    products = items.get("Products")
    if products is None or len(products) == 0:
        raise ValueError(
            "invalid agent type '{}': at least one product must be defined".format(agent_type_name))
    else:
        logging.debug("loading {} product(s) for agent type '{}'".format(
            len(products), agent_type_name))
        result.set_products(products)

    return result


def _load_schema_file(file_path: str) -> models.Schema:
    file_path = os.path.abspath(file_path)
    yaml_dict = yaml_utils.must_load_file(file_path)

    if yaml_dict is None or not "AgentTypes" in yaml_dict:
        raise ValueError("at least one agent type must be defined")

    result = models.Schema(file_path)
    for name, items in yaml_dict.get("AgentTypes").items():
        logging.debug("loading agent type {}".format(name))
        if items is None:
            # we accept agent types with no details
            logging.warning(
                "definition of agent type '{}' is empty".format(name))
        else:
            result.add_agent_type(_extract_attributes(name, items))

    return result


class SchemaLoader:
    """ Class to load and parse schema files """
    @staticmethod
    def load_yaml_file(file_path: str) -> models.Schema:
        logging.info("loading schema file {}".format(file_path))
        try:
            return _load_schema_file(file_path)
        except Exception as e:
            raise ValueError(
                "failed to load schema file {}".format(file_path)) from e
