import logging
from collections import namedtuple
from .brew_repository import BrewInfo

TargetState = namedtuple("TargetState", ["heater_state", "cooler_state"])


class DecisionModule(object):
    def get_target_state(
        self,
        beer_temp: float,
        ambient_temp: float,
        heater_current_state: bool,
        cooler_current_state: bool,
        brew_info: BrewInfo,
    ) -> TargetState:

        # For now I'll ignore all other parameters. But, in the future, some smarter control algorithm will be implemented
        if beer_temp <= brew_info.min_temp:
            return TargetState(heater_state=True, cooler_state=False)

        if beer_temp > brew_info.max_temp:
            return TargetState(heater_state=False, cooler_state=True)

        return TargetState(heater_state=False, cooler_state=False)
