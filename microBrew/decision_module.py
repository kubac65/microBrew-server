class DecisionModule(object):
    def __init__(self, brew_repo):
        self.__brew_repo = brew_repo

    def get_desired_state(self, brew_id, beer_temp, ambient_temp, initial_heater_state):
        min_temp, max_temp = self.__brew_repo.get_temp_range(brew_id)

        # For now I'll ignore all other parameters. But, in the future, some smarter control algorithm will be implemented

        if beer_temp <= min_temp:
            return (True, min_temp, max_temp)

        else:
            return (False, min_temp, max_temp)