from abc import ABC, abstractmethod
from typing import Dict
from datetime import date
from yield_curve.common.curve.Curve import Curve


class CurveBundle(ABC):
    """
    Interface to represent a group of curves built for a single currency.
    """

    @abstractmethod
    def get_valuation_date(self) -> date:
        """
        Get the valuation date of the curve bundle.
        :return: Valuation date as a datetime.date.
        """
        pass

    @abstractmethod
    def get_ccy(self) -> str:
        """
        Get the currency of the curve bundle.
        :return: Currency as a string.
        """
        pass

    @abstractmethod
    def get_discount_curve(self) -> Curve:
        """
        Get the discount curve for the currency.
        :return: Discount curve.
        """
        pass

    @abstractmethod
    def get_projection_curves(self) -> Dict[str, Curve]:
        """
        Get the projection curves as a dictionary.
        :return: A dictionary where the key is a string and the value is a Curve.
        """
        pass

    @abstractmethod
    def get_csa_discount_curves(self) -> Dict[str, Curve]:
        """
        Get the CSA discount curves as a dictionary.
        :return: A dictionary where the key is a string and the value is a Curve.
        """
        pass

    @abstractmethod
    def get_projection_curve(self, float_index_cd: str) -> Curve:
        """
        Get a specific projection curve.
        :param float_index_cd: Index code as a string.
        :return: Projection curve corresponding to the given index code.
        """
        pass

    @abstractmethod
    def get_projection_fixing(self, float_index_cd: str) -> float:
        """
        Get a specific projection fixing.
        :param float_index_cd: Index code as a string.
        :return: Projection fixing as a float.
        """
        pass

    @abstractmethod
    def get_projection_fixings(self) -> Dict[str, float]:
        """
        Get all projection fixings as a dictionary.
        :return: A dictionary where the key is a string and the value is a float.
        """
        pass

    @abstractmethod
    def get_fx_spot_rates(self) -> Dict[str, float]:
        """
        Get FX spot rates as a dictionary.
        :return: A dictionary where the key is a string and the value is a float.
        """
        pass
