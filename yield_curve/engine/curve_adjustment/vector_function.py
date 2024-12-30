from abc import ABC, abstractmethod
from typing import List


class VectorFunction(ABC):
    """
    Interface for a vector function.
    """

    @abstractmethod
    def dimension(self) -> int:
        """
        Gets the dimension of the vector function.
        :return: The dimension as an integer.
        """
        pass

    @abstractmethod
    def value(self, x: List[float]) -> List[float]:
        """
        Computes the value of the function for the given input vector.
        :param x: A list of floats representing the input vector.
        :return: A list of floats representing the output vector.
        :raises EngineException: If an error occurs during computation.
        """
        pass
