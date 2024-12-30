from yield_curve.engine.date.named import Named


class HolidayCalendarId(Named):
    """
    An identifier for a holiday calendar.
    Implements the Named interface.
    """

    def __init__(self, name: str):
        """
        Initializes the holiday calendar ID with a unique name.
        :param name: The unique name of the holiday calendar.
        """
        self._name = name

    def get_name(self) -> str:
        """
        Gets the unique name of the holiday calendar.
        :return: The name of the holiday calendar.
        """
        return self._name

    @staticmethod
    def of(name: str):
        """
        Creates an instance of HolidayCalendarId with the specified name.
        :param name: The unique name for the holiday calendar.
        :return: An instance of HolidayCalendarId.
        """
        return HolidayCalendarId(name)
