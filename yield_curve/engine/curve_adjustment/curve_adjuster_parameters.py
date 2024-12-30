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

from typing import List

from yield_curve.common.curve.Exception.EngineException import EngineException
from yield_curve.common.curve.interpolation_method import InterpolationMethod


class CurveAdjusterParams:
    OVERLAP_THRESHOLD = 7  # One week

    def __init__(self, index: str, short_dates: List[float], mid_dates: List[float],
                 long_dates: List[float], interp_method: InterpolationMethod, high_res: bool):
        self.index = index
        self.short_dates = short_dates
        self.mid_dates = mid_dates
        self.long_dates = long_dates
        self.interp_method = interp_method
        self.high_res = high_res
        self.num_short_mid_overlap_points = -1
        self.num_mid_long_overlap_points = -1

    def get_short_dates(self) -> List[float]:
        return self.short_dates

    def get_mid_dates(self) -> List[float]:
        return self.mid_dates

    def get_long_dates(self) -> List[float]:
        return self.long_dates

    def get_interpolation_method(self) -> InterpolationMethod:
        return self.interp_method

    def is_high_res(self) -> bool:
        return self.high_res

    def get_index(self) -> str:
        return self.index

    def get_num_short_mid_overlap_points(self) -> int:
        if self.num_short_mid_overlap_points != -1:
            return self.num_short_mid_overlap_points

        overlap = 0
        if len(self.short_dates) == 0:
            self.num_short_mid_overlap_points = 0
            return overlap

        for i in range(len(self.short_dates)):
            if self.short_dates[i] <= self.mid_dates[0] + self.OVERLAP_THRESHOLD:
                overlap += 1
            else:
                break

        self.num_short_mid_overlap_points = overlap
        return overlap

    def get_short_mid_overlap_dates(self, valuation_date: float) -> List[float]:
        overlap_dates = [0] * (self.get_num_short_mid_overlap_points() + 1)
        if len(overlap_dates) == 1:
            overlap_dates[0] = valuation_date
            return overlap_dates

        overlap_dates[0] = valuation_date
        i = 1
        for date in self.short_dates[:self.get_num_short_mid_overlap_points()]:
            overlap_dates[i] = date
            i += 1
        return overlap_dates

    def get_num_mid_long_overlap_points(self) -> int:
        if self.num_mid_long_overlap_points != -1:
            return self.num_mid_long_overlap_points

        overlap = 0
        if len(self.mid_dates) == 0:
            self.num_mid_long_overlap_points = 0
            return overlap

        for i in range(len(self.mid_dates)):
            if self.mid_dates[i] <= self.long_dates[0] + self.OVERLAP_THRESHOLD:
                overlap += 1
            else:
                break

        self.num_mid_long_overlap_points = overlap
        return overlap

    def get_mid_long_overlap_dates(self, valuation_date: float) -> List[float]:
        overlap_dates = [0] * (self.get_num_mid_long_overlap_points() + 1)
        if len(overlap_dates) == 1:
            overlap_dates[0] = valuation_date
            return overlap_dates

        overlap_dates[0] = valuation_date
        i = 1
        for date in self.mid_dates[:self.get_num_mid_long_overlap_points()]:
            overlap_dates[i] = date
            i += 1
        return overlap_dates

    def get_num_curve_points(self) -> int:
        overlap_pts = self.get_num_short_mid_overlap_points() + self.get_num_mid_long_overlap_points()
        # ToDo
        overlap_pts = 0
        return len(self.short_dates) + len(self.mid_dates) + len(self.long_dates) - overlap_pts

    def get_num_total_points(self) -> int:
        return len(self.short_dates) + len(self.mid_dates) + len(self.long_dates)

    def get_curve_dates(self, valuation_date: float, curve_max_date: float) -> List[float]:
        short_mid_overlap = self.get_num_short_mid_overlap_points()
        mid_long_overlap = self.get_num_mid_long_overlap_points()

        if len(self.long_dates) == 0:
            if len(self.short_dates) == 0 and len(self.mid_dates) == 0:
                # raise EngineException("Must have at least one long maturity")
                return [valuation_date, curve_max_date]

        extrap_curve = len(self.long_dates) > 0 and self.long_dates[-1] < curve_max_date

        curve_dates = [0] * (self.get_num_curve_points() + (1 if extrap_curve else 0))
        i = 0
        curve_dates[i] = valuation_date
        i += 1

        for date in self.short_dates[:-short_mid_overlap]:
            curve_dates[i] = date
            i += 1
        for date in self.mid_dates[:-mid_long_overlap]:
            curve_dates[i] = date
            i += 1
        for date in self.long_dates:
            curve_dates[i] = date
            i += 1

        if extrap_curve:
            curve_dates[i] = curve_max_date

        return curve_dates
