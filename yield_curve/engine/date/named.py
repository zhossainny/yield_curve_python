from abc import ABC, abstractmethod


class Named(ABC):
    """
    A named instance.
    This abstract base class is used to define objects that can be identified by a unique name.
    The name contains enough information to be able to recreate the instance.
    """

    @staticmethod
    def of(type_cls, name: str):
        """
        Obtains an instance of the specified named type by name.
        This method simulates reflection in Java using dynamic method invocation.

        :param type_cls: The named type with the 'of' method
        :param name: The name to find
        :return: The instance of the named type
        :raises ValueError: if the specified name could not be found
        """
        try:
            return type_cls.of(name)
        except AttributeError as e:
            raise ValueError(f"'of' method not found in {type_cls}") from e

    @abstractmethod
    def get_name(self) -> str:
        """
        Gets the unique name of the instance.
        The name contains enough information to be able to recreate the instance.
        :return: The unique name
        """
        pass
