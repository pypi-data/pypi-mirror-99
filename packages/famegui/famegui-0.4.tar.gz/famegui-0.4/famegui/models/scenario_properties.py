import logging
import copy


class ScenarioProperties:
    DEFAULT_VALUES = {
        "RunId": 1,
        "Simulation": {
            "StartTime": "2011-12-31_23:58:00",
            "StopTime": "2012-12-30_23:58:00",
            "RandomSeed": 1,
        },
        "Output": {
            "Interval": 100,
            "Process": 0,
        },
    }

    def __init__(self, values={}):
        self._values = copy.deepcopy(values)

    def init_missing_values(self) -> bool:
        """ Ensure all expected values are initialized, and return True if some missing fields were completed """
        previous_values = self._values
        self._values = {**self.DEFAULT_VALUES, **self._values}
        if self._values != previous_values:
            logging.info("some scenario properties have been initialized to their default value")
            return True
        return False

    @property
    def values(self):
        return self._values

    @property
    def simulation_start_time(self) -> str:
        return self._values["Simulation"]["StartTime"]

    def set_simulation_start_time(self, value: str):
        self._values["Simulation"]["StartTime"] = value

    @property
    def simulation_stop_time(self) -> str:
        return self._values["Simulation"]["StopTime"]

    def set_simulation_stop_time(self, value: str):
        self._values["Simulation"]["StopTime"] = value

    @property
    def simulation_random_seed(self) -> int:
        return self._values["Simulation"]["RandomSeed"]

    def set_simulation_random_seed(self, value: int):
        assert isinstance(value, int)
        self._values["Simulation"]["RandomSeed"] = value

    @property
    def output_interval(self) -> int:
        return self._values["Output"]["Interval"]

    def set_output_interval(self, value: int):
        assert isinstance(value, int)
        self._values["Output"]["Interval"] = value

    @property
    def output_process(self) -> int:
        return self._values["Output"]["Process"]

    def set_output_process(self, value: int):
        assert isinstance(value, int)
        self._values["Output"]["Process"] = value
