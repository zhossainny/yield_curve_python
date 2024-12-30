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

from typing import Optional

from yield_curve.common.curve.Curve import Curve


class FxContext:
    def __init__(
        self,
        base_discount_curve: Curve,
        base_projection_curve: Curve,
        base_projection_fixing: float,
    ):
        """
        Initialize the FxContext object.

        :param base_discount_curve: Discount curve for the base leg.
        :param base_projection_curve: Projection curve for the base leg.
        :param base_projection_fixing: FX spot rate in units of base currency.
        """
        self._base_discount_curve: Curve = base_discount_curve
        self._base_projection_curve: Curve = base_projection_curve
        self._base_projection_fixing: float = base_projection_fixing
        self._fx_spot: Optional[float] = None
        self._points_divisor: float = 10000.0  # Typically 10000 for basis points
        self._inverse_quoted: bool = False

    def get_fx_spot(self) -> Optional[float]:
        """Get the FX spot rate."""
        return self._fx_spot

    def set_fx_spot(self, fx_spot: float):
        """Set the FX spot rate."""
        self._fx_spot = fx_spot

    def is_inverse_quoted(self) -> bool:
        """Check if the FX spot is inversely quoted."""
        return self._inverse_quoted

    def set_inverse_quoted(self, inverse_quoted: bool):
        """Set whether the FX spot is inversely quoted."""
        self._inverse_quoted = inverse_quoted

    def get_points_divisor(self) -> float:
        """Get the points divisor."""
        return self._points_divisor

    def set_points_divisor(self, points_divisor: float):
        """Set the points divisor."""
        self._points_divisor = points_divisor

    def get_base_discount_curve(self) -> Curve:
        """Get the base discount curve."""
        return self._base_discount_curve

    def get_base_projection_curve(self) -> Curve:
        """Get the base projection curve."""
        return self._base_projection_curve

    def get_base_projection_fixing(self) -> float:
        """Get the base projection fixing."""
        return self._base_projection_fixing
