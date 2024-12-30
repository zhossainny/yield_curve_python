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

from datetime import date
from typing import Optional

from yield_curve.common.curve.Curve import Curve
from yield_curve.common.curve.Exception.EngineException import EngineException
from yield_curve.engine.calib_instrument.calibration_context import CalibrationContext
from yield_curve.engine.curve_adjustment.curve_adjuster import CurveAdjuster
from yield_curve.engine.date.day_count import DayCount


# ToDo TEST IT. Formula has been set, same approach as other swap type, but has not been tested
class FuturePricingFunction:
    def __init__(
            self,
            ctx: CalibrationContext,
            value_date: date,
            float_index_id: int,
            start_date: date,
            end_date: date,
            price: float,
            convex_add: float,
    ):
        # Fetch FloatIndex data
        float_index_data = ctx.get_database().get_data_row("FloatIndex", float_index_id)
        self.float_index_cd = float_index_data.get("Code")
        day_count_str = float_index_data.get("DayCount")

        # Initialize DayCount
        day_count = DayCount.of(day_count_str)
        self.value_date = self.date_to_double(value_date)
        self.start_date = self.date_to_double(start_date)
        self.end_date = self.date_to_double(end_date)

        # Compute accrual factor and target rate
        self.accrual_factor = day_count.year_fraction(start_date, end_date)
        self.target_rate = ((100.0 - price) / 100.0) - convex_add

    @staticmethod
    def date_to_double(input_date: date) -> float:
        # Convert date to float (assuming we have a base epoch)
        return (input_date - date(1970, 1, 1)).days

    def value(self, adjuster: CurveAdjuster) -> float:
        # Fetch the appropriate curve
        curve: Optional[Curve]
        if adjuster.get_anchor_params().get_index() == self.float_index_cd:
            curve = adjuster.get_anchor_curve()
        elif adjuster.get_basis_params().get_index() == self.float_index_cd:
            curve = adjuster.get_basis_curve()
        else:
            raise EngineException(f"Cannot find curve for index {self.float_index_cd}")

        # Interpolation and discounting
        swap_basis = adjuster.get_anchor_mid_long_basis_curve()
        max_basis_date = swap_basis.get_x()[-1]

        t1 = (self.start_date - self.value_date) / 365.0
        z1 = curve.interpolate(self.start_date) + swap_basis.interpolate(min(self.start_date, max_basis_date))
        df1 = pow(2.71828, -z1 * t1)

        t2 = (self.end_date - self.value_date) / 365.0
        z2 = curve.interpolate(self.end_date) + swap_basis.interpolate(min(self.end_date, max_basis_date))
        df2 = pow(2.71828, -z2 * t2)

        # Calculate the forward rate
        rate = (df1 / df2 - 1.0) / self.accrual_factor
        return rate - self.target_rate

    def curve_date(self) -> float:
        return self.end_date
