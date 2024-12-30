from abc import ABC, abstractmethod
from datetime import timedelta


class InstrumentType:
    FIXING = "FIXING"
    FRA = "FRA"
    DATED_FRA = "DATED_FRA"
    FUTURE = "FUTURE"
    SWAP = "SWAP"
    BASIS_FRA = "BASIS_FRA"
    BASIS_FUTURE = "BASIS_FUTURE"
    BASIS_SWAP = "BASIS_SWAP"
    FX_SPOT = "FX_SPOT"
    FX_POINT = "FX_POINT"
    CROSS_CCY_BASIS = "CROSS_CCY_BASIS"
    DI_FUTURE = "DI_FUTURE"


class CalibInstrument(ABC):
    def __init__(self, settlement_lag: int, settlement_calendar_cd: str):
        self._settlement_lag = settlement_lag
        self._settlement_calendar_cd = settlement_calendar_cd

    @abstractmethod
    def get_instrument_type(self) -> InstrumentType:
        pass

    @abstractmethod
    def get_order(self) -> float:
        pass

    @abstractmethod
    def get_ticker(self) -> str:
        pass

    @abstractmethod
    def resolve(self, context, value_date):
        pass

    def get_settlement_lag(self) -> int:
        return self._settlement_lag

    def get_settlement_calendar(self) -> str:
        return self._settlement_calendar_cd

    def set_fx_context(self, context):
        # By default, do nothing
        pass

    def __lt__(self, other):
        """Implements comparison based on type, then by order."""
        if not isinstance(other, CalibInstrument):
            return NotImplemented
        type_compare = (self.get_instrument_type() > other.get_instrument_type()) - (
            self.get_instrument_type() < other.get_instrument_type()
        )
        if type_compare != 0:
            return type_compare < 0
        return self.get_order() < other.get_order()

    def get_settle_date(self, context, value_date):
        """Compute the settlement date based on the settlement lag."""
        holiday_calendar = context.get_calendar(self.get_settlement_calendar())
        return holiday_calendar.shift(value_date, self.get_settlement_lag())


# Holiday Calendar from opengamma

