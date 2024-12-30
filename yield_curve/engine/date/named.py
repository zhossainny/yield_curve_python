# Licensed under the Apache License, Version 2.0
# Copyright 2024 Zahid Hossain <zhossainny@gmail.com>
#
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
