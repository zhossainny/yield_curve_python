from datetime import datetime, timedelta


class DateConvert:
    """
    Utility class for converting between LocalDate and double representations.
    """

    @staticmethod
    def local_date_to_double(local_date):
        """
        Convert a LocalDate (datetime.date) to a double representation.
        The double is the number of days since 1970-01-01 (epoch) plus 25569.0.
        :param local_date: The date to convert (datetime.date).
        :return: A double representation of the date.
        """
        epoch_start = datetime(1970, 1, 1).date()
        days_since_epoch = (local_date - epoch_start).days
        return days_since_epoch + 25569.0

    @staticmethod
    def double_to_local_date(date_double):
        """
        Convert a double representation of a date back to a LocalDate (datetime.date).
        The double is assumed to be the number of days since 1970-01-01 (epoch) plus 25569.0.
        :param date_double: The double representation of the date.
        :return: A datetime.date corresponding to the double.
        """
        epoch_start = datetime(1970, 1, 1).date()
        days_since_epoch = int(round(date_double - 25569.0))
        return epoch_start + timedelta(days=days_since_epoch)
