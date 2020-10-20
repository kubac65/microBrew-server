from .brew_repository import BrewRepository


class DecisionModule(object):
    def __init__(self, brew_repo: BrewRepository):
        self.__brew_repo = brew_repo

    def get_desired_state(
        self,
        brew_id: int,
        beer_temp: float,
        ambient_temp: float,
        heater_current_state: bool,
        cooler_current_state: bool,
    ) -> (bool, bool, float, float):
        brew_info = self.__brew_repo.get_brew_info(brew_id)

        if not brew_info.active:
            return (False, False, 0, 0)

        # For now I'll ignore all other parameters. But, in the future, some smarter control algorithm will be implemented
        if beer_temp <= brew_info.min_temp:
            return (True, False, brew_info.min_temp, brew_info.max_temp)

        else:
            return (False, False, brew_info.min_temp, brew_info.max_temp)
