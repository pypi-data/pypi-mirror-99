import logging
import os
import sys

from fameio.scripts.make_config import run as run_make_config


def generate_protobuf_from_scenario_yaml_file(working_dir: str, input_path: str, output_path: str):
    logging.info("generating protobuf output to {}".format(output_path))
    assert os.path.isabs(output_path)

    try:
        logging.info("changing current diretory to {}".format(working_dir))
        os.chdir(working_dir)

        config = {
            "log_level": "INFO",
            "output_file": output_path,
            "log_file": None,
        }
        run_make_config(input_path, config)
    except Exception as e:
        logging.error("failed to generate protobuf output: {}".format(e))
        raise ValueError(
            "failed to generate the protobuf output, see the logs for more details")


def main():
    if len(sys.argv) != 2:
        print("Input scenario file must be passed in argument")
        sys.exit(1)

    input_path = os.path.abspath(sys.argv[1])
    this_dir = os.path.dirname(os.path.abspath(__file__))
    working_dir = os.path.abspath(
        os.path.join(this_dir, "../fame_working_dir"))
    print("Working dir: {}".format(working_dir))
    generate_protobuf_from_scenario_yaml_file(
        working_dir, input_path, input_path + ".pb")


if __name__ == "__main__":
    main()
