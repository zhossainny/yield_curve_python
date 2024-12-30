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

class EngineException(Exception):
    """
    Base exception class for engine-related errors.
    Inherits from the built-in Exception class.
    """

    def __init__(self, msg=None, cause=None):
        """
        Initialize the EngineException.
        :param msg: Error message (str).
        :param cause: Original exception (optional).
        """
        super().__init__(msg)
        self.cause = cause
