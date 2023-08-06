import logging
import os
import yaml
import typing

from famegui.models import Scenario, ScenarioProperties, Agent, Contract, layout_agents
import famegui.models.yaml_utils as yaml_utils


def _extract_contract(contract_number, contract_dict) -> Contract:
    logging.debug("loading contract number {}".format(contract_number))
    try:
        product_name = yaml_utils.must_get_str_key(
            contract_dict, "ProductName")
        sender_id = yaml_utils.must_get_int_key(contract_dict, "SenderId")
        receiver_id = yaml_utils.must_get_str_key(contract_dict, "ReceiverId")
        delivery_interval_in_steps = yaml_utils.get_int_key_or(
            contract_dict, "DeliveryIntervalInSteps", 0)
        first_delivery_time = yaml_utils.get_int_key_or(
            contract_dict, "FirstDeliveryTime", 0)
        return Contract(sender_id, receiver_id, product_name, delivery_interval_in_steps, first_delivery_time)
    except Exception as e:
        raise ValueError(
            "failed to load contract number '{}'".format(contract_number)) from e


def _extract_agent(agent_number, agent_dict) -> Agent:
    logging.debug("loading agent number {}".format(agent_number))
    try:
        agent_id = yaml_utils.must_get_int_key(agent_dict, "Id")
        if agent_id < 0:
            raise ValueError(
                "invalid id '{}' (must be a positive integer)".format(agent_id))
        agent_type = yaml_utils.must_get_str_key(agent_dict, "Type")
        agent = Agent(agent_id, agent_type)

        # load attributes
        attr_dict = agent_dict.get("Attributes")
        if attr_dict is not None:
            for name, value in attr_dict.items():
                agent.add_attribute(name, value)

        # load X,Y
        if "Ext" in agent_dict and "GUI" in agent_dict.get("Ext"):
            gui_dict = agent_dict.get("Ext").get("GUI")
            if "DisplayXY" in gui_dict:
                [x, y] = gui_dict.get("DisplayXY")
                agent.set_display_xy(x, y)

        return agent
    except Exception as e:
        raise ValueError(
            "failed to load agent number {}".format(agent_number)) from e


def _check_all_agents_have_display_coords(agents):
    if len(agents) == 0:
        return True
    for _, a in agents.items():
        if a.display_xy is None:
            return False
        return True


def _agent_to_dict(agent: Agent):
    result = {}
    result["Type"] = agent.type_name
    result["Id"] = agent.id
    result["Attributes"] = agent.attributes
    result["Ext"] = {
        "GUI": {
            "DisplayXY": agent.display_xy,
        }
    }
    return result


def _contract_to_dict(contract: Contract):
    result = {}
    result["ProductName"] = contract.product_name
    result["SenderId"] = contract.sender_id
    result["ReceiverId"] = contract.receiver_id
    result["DeliveryIntervalInSteps"] = 2
    result["FirstDeliveryTime"] = 1
    return result


def _get_node_children(dict, node_name):
    """ always return a valid dict (possibly empty) containing the children of the given node """
    if dict is None or node_name not in dict:
        return {}
    node = dict.get(node_name)
    if node is None:
        return {}
    return node


class CustomYamlLoader(yaml.loader.SafeLoader):
    @staticmethod
    def load_file(file_path):
        def include_constructor(loader, node):
            return loader.construct_scalar(node)

        logging.info("loading scenario file {}".format(file_path))
        CustomYamlLoader.add_constructor(u'!include', include_constructor)
        try:
            with open(file_path) as f:
                return yaml.load(f, Loader=CustomYamlLoader)
        except Exception as e:
            raise RuntimeError(
                "failed to load yaml file '{}'".format(file_path)) from e


class ScenarioLoader:
    @staticmethod
    def load_yaml_file(file_path: str) -> Scenario:
        """ Load (read and parse) a YAML scenario file """
        file_path = os.path.abspath(file_path)
        yaml_dict = CustomYamlLoader.load_file(file_path)

        scenario = Scenario()

        # properties
        if "GeneralProperties" in yaml_dict:
            logging.info("found general properties")
            scenario.set_properties(ScenarioProperties(
                yaml_dict["GeneralProperties"]))

        # schema name
        if "Schema" in yaml_dict:
            scenario.set_schema_path(yaml_dict["Schema"])
            logging.info("found reference to schema file {}".format(
                scenario.schema_path))
        else:
            logging.warning("no schema file defined")

        # agents
        current_agent_number = 1
        for node in _get_node_children(yaml_dict, "Agents"):
            agent = _extract_agent(current_agent_number, node)
            scenario.add_agent(agent)
            current_agent_number += 1
        logging.info("loaded {} agent(s)".format(len(scenario.agents)))

        # contracts
        current_contract_number = 1
        for node in _get_node_children(yaml_dict, "Contracts"):
            scenario.add_contract(
                _extract_contract(current_contract_number, node))
            current_contract_number += 1
        logging.info("loaded {} contract(s)".format(len(scenario.contracts)))

        # check if layout generation is necessary
        if not _check_all_agents_have_display_coords(scenario.agents):
            layout_agents(scenario)
        assert _check_all_agents_have_display_coords(scenario.agents)

        return scenario

    @staticmethod
    def save_to_yaml_file(scenario: Scenario, file_path: str):
        """ Save the given scenario to a YAML file """
        logging.info("saving scenario to file {}".format(file_path))
        assert os.path.isabs(file_path)

        output = {}
        output["GeneralProperties"] = scenario.properties.values

        scenario_dir = os.path.dirname(file_path)
        schema_rel_path = os.path.relpath(
            scenario.schema_path, scenario_dir).replace('\\', '/')
        logging.info(
            "schema path saved in scenario file: {}".format(schema_rel_path))

        output["Agents"] = []
        for a in scenario.agents.values():
            output["Agents"].append(_agent_to_dict(a))

        output["Contracts"] = []
        for c in scenario.contracts:
            output["Contracts"].append(_contract_to_dict(c))

        try:
            with open(file_path, "w") as f:
                # we can't use the yaml writer to encode the "!include" extension so we do it manually
                f.write('Schema: !include "{}"\n'.format(schema_rel_path))
                yaml.dump(output, f)
        except Exception as e:
            raise RuntimeError(
                "failed to save scenario to file '{}'".format(file_path)) from e
