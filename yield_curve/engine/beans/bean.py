from abc import ABC, abstractmethod
from typing import Set, Generic, TypeVar

R = TypeVar('R')

class MetaBean(ABC):
    """
    Abstract class representing the meta information about a Bean.
    """

    @abstractmethod
    def meta_property(self, property_name: str):
        """
        Retrieve the meta-property for the given property name.
        :param property_name: Name of the property
        :return: Meta-property object
        """
        pass

    @abstractmethod
    def meta_property_map(self) -> dict:
        """
        Retrieve a mapping of property names to meta-properties.
        :return: A dictionary mapping property names to meta-properties
        """
        pass

class Property(Generic[R]):
    """
    A class representing a property of a Bean.
    """
    def __init__(self, value: R):
        self.value = value

class Bean(ABC):
    """
    Represents a Bean, which has meta-properties and properties.
    """

    @abstractmethod
    def meta_bean(self) -> MetaBean:
        """
        Get the MetaBean associated with this Bean.
        :return: MetaBean object
        """
        pass

    def property(self, property_name: str) -> Property:
        """
        Get the Property object for the specified property name.
        :param property_name: The name of the property
        :return: Property object
        """
        return self.meta_bean().meta_property(property_name).create_property(self)

    def property_names(self) -> Set[str]:
        """
        Get the set of all property names.
        :return: Set of property names
        """
        return set(self.meta_bean().meta_property_map().keys())
