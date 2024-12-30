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
import unittest

# from yield_curve.engine.calib_instrument.calibration_context import CalibrationContext
from yield_curve.engine.calib_instrument.calibration_context2 import CalibrationContext2, DataBase


class CalibrationContextTest(unittest.TestCase):
    def build_test_context(self) -> CalibrationContext2:
        self.db = DataBase()

        # Define New York holidays
        ny_holidays = [
            date(2021, 1, 1), date(2021, 1, 18), date(2021, 2, 15), date(2021, 5, 31),
            date(2021, 7, 5), date(2021, 9, 6), date(2021, 11, 25), date(2021, 12, 24),
            date(2022, 1, 17), date(2022, 2, 21), date(2022, 5, 30), date(2022, 7, 4),
            date(2022, 9, 5), date(2022, 11, 24), date(2022, 12, 26), date(2080, 1, 1)
        ]

        # Define London holidays
        london_holidays = [
            date(2021, 1, 1), date(2021, 4, 2), date(2021, 4, 5), date(2021, 5, 3),
            date(2021, 5, 31), date(2021, 8, 30), date(2021, 12, 27), date(2021, 12, 28),
            date(2022, 1, 3), date(2022, 4, 15), date(2022, 4, 18), date(2022, 5, 2),
            date(2022, 6, 2), date(2022, 6, 3), date(2022, 8, 29), date(2080, 1, 1)
        ]

        # Add New York holidays to the database
        holiday_calendar_table = []
        for holiday in ny_holidays:
            holiday_calendar_table.append({"Code": "New York", "Date": holiday})

        # Add London holidays to the database
        for holiday in london_holidays:
            holiday_calendar_table.append({"Code": "London", "Date": holiday})

        self.db.tables["HolidayCalendar"] = holiday_calendar_table

        # Add FloatIndex data to the database
        float_index_data = [
            {"Code": "USD1D", "DayCount": "A360", "FixingLag": 2, "Currency": "USD", "BusinessDayAdjustment": "NONE",
             "Tenor": "1D"},
            {"Code": "USD3M", "DayCount": "A360", "FixingLag": 2, "Currency": "USD", "BusinessDayAdjustment": "NONE",
             "Tenor": "3M"},
            {"Code": "EUR1M", "DayCount": "A360", "FixingLag": 2, "Currency": "EUR", "BusinessDayAdjustment": "NONE",
             "Tenor": "1M"},
            {"Code": "EUR6M", "DayCount": "A360", "FixingLag": 2, "Currency": "EUR", "BusinessDayAdjustment": "NONE",
             "Tenor": "6M"},
            {"Code": "JPY3M", "DayCount": "A360", "FixingLag": 2, "Currency": "JPY", "BusinessDayAdjustment": "NONE",
             "Tenor": "3M"},
            {"Code": "USD6M", "DayCount": "A360", "FixingLag": 2, "Currency": "USD", "BusinessDayAdjustment": "NONE",
             "Tenor": "6M"},
            {"Code": "BRL1D", "DayCount": "A252", "FixingLag": 2, "Currency": "BRL", "BusinessDayAdjustment": "NONE",
             "Tenor": "1D"}
        ]

        self.db.tables["FloatIndex"] = float_index_data

        # Return the calibration context
        return CalibrationContext2(self.db)

    def test_float_index_data(self):
        # Build the context and retrieve the database
        ctx = self.build_test_context()
        db = ctx.db

        # Verify New York calendar holidays
        ny_calendar = ctx.get_calendar("New York")
        self.assertIn(date(2022, 5, 30), ny_calendar["holidays"])
        # self.assertIn(date(2021, 1, 1), ny_calendar["holidays"])

        # Verify London calendar holidays
        lon_calendar = ctx.get_calendar("London")
        self.assertIn(date(2021, 12, 27), lon_calendar["holidays"])
        self.assertIn(date(2021, 1, 1), lon_calendar["holidays"])

        # Verify FloatIndex table
        float_index_table = db.tables.get("FloatIndex", [])
        self.assertEqual(len(float_index_table), 7)

        # Check specific data in FloatIndex table
        usd1d = next(row for row in float_index_table if row["Code"] == "USD1D")
        self.assertEqual(usd1d["DayCount"], "A360")
        self.assertEqual(usd1d["Currency"], "USD")
        self.assertEqual(usd1d["Tenor"], "1D")

        eur6m = next(row for row in float_index_table if row["Code"] == "EUR6M")
        self.assertEqual(eur6m["DayCount"], "A360")
        self.assertEqual(eur6m["Currency"], "EUR")
        # self.assertEqual(eur6m["Tenor"], "6M")

