class MicroBrewError(Exception):
    def __init__(self, e):
        Exception.__init__(e)


class MalformedMessageError(MicroBrewError):
    def __init__(self):
        pass
