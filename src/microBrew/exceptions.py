class MicroBrewError(Exception):
    """
    Generic MicroBrew exception
    """

    pass


class MalformedMessageError(MicroBrewError):
    """
    Raised when malformed message is received from the sensor
    """

    pass
