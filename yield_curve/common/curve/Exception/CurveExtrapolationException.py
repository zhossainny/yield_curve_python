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

from yield_curve.common.curve.Exception.CurveException import CurveException


class CurveExtrapolationException(CurveException):
    """
    Exception class for errors related to curve extrapolation.
    Inherits from CurveException.
    """

    def __init__(self, msg=None, cause=None):
        """
        Initialize the CurveExtrapolationException.
        :param msg: Error message (str).
        :param cause: Original exception (optional).
        """
        super().__init__(msg, cause)
