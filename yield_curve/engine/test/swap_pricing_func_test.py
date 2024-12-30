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
from datetime import date

import numpy as np

from yield_curve.common.curve.CurveImp import CurveImpl
from yield_curve.common.curve.interpolation_method import InterpolationMethod
from yield_curve.engine.calib_instrument.calibration_context import CalibrationContext
from yield_curve.engine.curve_adjustment.curve_adjuster import CurveAdjuster
from yield_curve.engine.curve_adjustment.curve_adjuster_parameters import CurveAdjusterParams
from yield_curve.engine.pricing_functions.swap_pricing_function import SwapPricingFunction
from yield_curve.engine.test.calib_context_test import CalibrationContextTest


class SwapPricingFunctionTest(unittest.TestCase):
    def testSwapPricingFunction(self):
        temp = CalibrationContextTest()
        self.ctx = temp.build_test_context()
        # Step 2: Define curve data
        dates = [44287.0, 44317.0, 44348.0, 44378.0, 44409.0, 44440.0, 44501.0, 44571.0, 45383.0,
                 46113.0, 47039.0, 47966.0, 51592.0, 53418.0, 54879.0]
        rates = [0.02, 0.01, 0.011, 0.012, 0.015, 0.02, 0.025, 0.027, 0.026, 0.024, 0.023, 0.0235, 0.024, 0.0235, 0.024]

        dates_array = np.array(dates)
        rates_array = np.array(rates)
        initial_curve = CurveImpl(dates_array, rates_array, InterpolationMethod.LINEAR_DF)
        anchor_params = CurveAdjusterParams("USD3L", [], [44317.0, 44348.0, 44378.0, 44470.0], [44652.0, 45017.0, 45383.0, 46113.0, 47939.0, 49766.0, 53418.0, 54879.0]
                                           , InterpolationMethod.LINEAR_DF,False)
        basis_params = CurveAdjusterParams("USD3L",[], [], [], InterpolationMethod.LINEAR_DF, False)

        adjuster = CurveAdjuster(dates[0], 80811.0, initial_curve, initial_curve, None, True, anchor_params, basis_params)

        # Step 3: Define swap parameters
        value_date = date(2021, 4, 1)
        settle_date = date(2021, 4, 5)
        float_index_id = 1
        fixed_freq_cd = "6M"
        fixed_day_count_cd = "ACT/365"
        fixed_business_day_cd = "ModifiedFollowing"
        float_freq_cd = "3M"
        float_day_count_cd = "ACT/360"
        float_business_day_cd = "ModifiedFollowing"
        calendar_cd = "New York"
        tenors = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 15.0, 20.0, 25.0]
        swap_rates = [
            0.02233706722445793, 0.02519560411994168, 0.027170311482402558,
            0.027401721129152255, 0.027401721129152255, 0.026195222962544635, 0.025314127876287163,
            0.02493034897177685, 0.02507246509192216, 0.0250418599814227,
            0.025051954969558744, 0.024309583113161285, 0.023665933921271944,
            0.023794699538525206
        ]
        # Step 4: Perform swap pricing for each tenor
        for i, tenor in enumerate(tenors):
            func = SwapPricingFunction(
                ctx=self.ctx,
                value_date=value_date,
                settle_date=settle_date,
                float_index_id=float_index_id,
                tenor=int(tenor),
                fixed_freq_cd=fixed_freq_cd,
                fixed_day_count_cd=fixed_day_count_cd,
                fixed_business_day_cd=fixed_business_day_cd,
                float_freq_cd=float_freq_cd,
                float_day_count_cd=float_day_count_cd,
                float_business_day_cd=float_business_day_cd,
                calendar_cd=calendar_cd,
                target_rate=0.00
            )
            result = func.value(adjuster)
            self.assertAlmostEqual(swap_rates[i], result, delta=1e-6)