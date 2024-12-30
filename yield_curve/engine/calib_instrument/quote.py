from enum import Enum


class QuoteField(Enum):
    PRICE = "PRICE"
    CONVEXITY_ADJ = "CONVEXITY_ADJ"


class Quote:
    def __init__(self, field: QuoteField, value: float):
        """
        Initializes the Quote object with a field and value.
        :param field: The field of the quote (e.g., PRICE, CONVEXITY_ADJ).
        :param value: The value of the quote.
        """
        self._field = field
        self._value = value

    def get_field(self) -> QuoteField:
        """
        Gets the field of the quote.
        :return: The field of the quote.
        """
        return self._field

    def get_value(self) -> float:
        """
        Gets the value of the quote.
        :return: The value of the quote.
        """
        return self._value
