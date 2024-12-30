from abc import ABC, abstractmethod

from yield_curve.engine.curve_adjustment.curve_adjuster import CurveAdjuster


class PricingFunction(ABC):
    @abstractmethod
    def value(self, adjuster: CurveAdjuster) -> float:
        """
        Calculate the value based on the given CurveAdjuster.

        :param adjuster: CurveAdjuster instance used for calculation.
        :return: Calculated value as a float.
        :raises EngineException: If an error occurs during the calculation.
        """
        pass

    @abstractmethod
    def curve_date(self) -> float:
        """
        Get the curve date.

        :return: Curve date as a float.
        """
        pass
