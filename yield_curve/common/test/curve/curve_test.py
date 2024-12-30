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

import unittest
import numpy as np
from yield_curve.common.curve.CurveImp import CurveImpl
from yield_curve.common.curve.linear_discount_factor_interpolator import LinearDiscountFactorInterpolator
from yield_curve.common.curve.interpolation_method import InterpolationMethod


class TestLinearDiscountFactorInterpolator(unittest.TestCase):
    def test_linear_interp_df(self):
        # Setup test data
        dates = np.array([
            44287.0, 44317.0, 44348.0, 44378.0,
            44470.0, 44652.0, 45017.0, 45383.0, 46113.0,
            47939.0, 49766.0, 51592.0, 53418.0, 54879.0
        ])
        rates = np.array([
            0.02, 0.01, 0.011, 0.012, 0.015,
            0.022, 0.025, 0.027, 0.026, 0.025, 0.024,
            0.0235, 0.0235, 0.024
        ])
        # Calculate discount factors using a loop
        df = np.zeros(len(dates))
        for i in range(len(dates)):
            t = (dates[i] - dates[0]) / 365.0
            df[i] = np.exp(-rates[i] * t)

        # Test dates for interpolation
        test_dates = np.array([
            44287.0, 44300.0, 44301.0, 44302.0, 44378.0, 44555.0
        ])
        result = np.zeros_like(test_dates, dtype=np.float64)

        # Create the curve
        curve = CurveImpl(dates, rates, InterpolationMethod.LINEAR_DF)
        # interpolator = LinearDiscountFactorInterpolator(curve)

        # Interpolate test dates
        for i, test_date in enumerate(test_dates):
            result[i] = curve.interpolate(test_date)

        # Validate interpolated results against expected results
        self.assertAlmostEqual(rates[0], result[0], delta=1e-12, msg="Rate at t=0")
        self.assertAlmostEqual(rates[3], result[4], delta=1e-12, msg="DF at knot point")

        # Additional validation for discount factors and derivatives
        rdf = np.zeros_like(result)
        drdf = np.zeros_like(result)

        for i, test_date in enumerate(test_dates):
            t = (test_date - dates[0]) / 365.0
            rdf[i] = np.exp(-result[i] * t)
            if i != 0:
                drdf[i] = rdf[i] - rdf[i - 1]

        self.assertAlmostEqual(drdf[2], drdf[3], delta=1e-12, msg="First derivative should be constant")

        # Recalculate interpolated results for further validation
        result2 = curve.interpolate_array(test_dates)
        for i, test_date in enumerate(test_dates):
            # result2[i] = interpolator.interpolate(test_date)
            self.assertAlmostEqual(result[i], result2[i], delta=1e-12, msg=f"Vector API at {i}")

        # Validate against expected discount factors
        expected = np.array([
            0.02, 0.00999767131800822, 0.00999780825927318, 0.009997945205537642, 0.012,
            0.01941697178973371
        ])
        for i, expected_value in enumerate(expected):
            self.assertAlmostEqual(expected_value, result[i], delta=1e-12, msg=f"Curve at {test_dates[i]}")
