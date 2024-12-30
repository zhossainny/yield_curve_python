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
