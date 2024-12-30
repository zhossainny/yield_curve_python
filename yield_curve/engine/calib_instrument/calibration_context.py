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

from typing import Dict, List, Set, Optional
from datetime import date
from enum import Enum

from yield_curve.common.curve.Exception.EngineException import EngineException
from yield_curve.engine.date.abs_holiday_calendar import HolidayCalendar
from yield_curve.engine.date.holiday_calendar_id import HolidayCalendarId
from yield_curve.engine.date.immutable_holiday_calendar import ImmutableHolidayCalendar
from yield_curve.engine.util.abs_data_field import DataField
from yield_curve.engine.util.abs_database import DataBase
from yield_curve.engine.util.data_field_immutable import DataFieldImmutable


# Placeholder types

class DayOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


# CalibrationContext class
class CalibrationContext:
    def __init__(self, db: DataBase):
        self.db = db
        self.float_index_map: Dict[DataField, int] = self.db.index(table_name="FloatIndex", field_name="Code")
        self.calendar_map: Dict[str, HolidayCalendar] = {}
        self.build_calendars()

    def get_database(self) -> DataBase:
        return self.db

    def get_float_index_id(self, name: str) -> int:
        key = DataFieldImmutable(name="Code", data_type="STRING", value=name)
        value = self.float_index_map.get(key)
        if value is None:
            raise EngineException(f"Float Index not found: {name}")
        return value

    def set_calendar(self, code: str, calendar: HolidayCalendar):
        self.calendar_map[code] = calendar

    def get_calendar(self, code: str) -> Optional[HolidayCalendar]:
        return self.calendar_map.get(code)

    def get_weekend_list(self, weekend_rule: Optional[str]) -> List[DayOfWeek]:
        code_to_dow = {
            "SU": DayOfWeek.SUNDAY,
            "MO": DayOfWeek.MONDAY,
            "TU": DayOfWeek.TUESDAY,
            "WE": DayOfWeek.WEDNESDAY,
            "TH": DayOfWeek.THURSDAY,
            "FR": DayOfWeek.FRIDAY,
            "SA": DayOfWeek.SATURDAY,
        }
        weekend_list: List[DayOfWeek] = []

        if weekend_rule is None:
            weekend_list.extend([DayOfWeek.SATURDAY, DayOfWeek.SUNDAY])
            return weekend_list

        if len(weekend_rule) >= 2:
            day = code_to_dow.get(weekend_rule[:2])
            if day is not None:
                weekend_list.append(day)

        if len(weekend_rule) == 4:
            day = code_to_dow.get(weekend_rule[2:4])
            if day is not None:
                weekend_list.append(day)

        return weekend_list

    def build_calendars(self):
        # Initialize the calendar map
        self.calendar_map: Dict[str, HolidayCalendar] = {}

        # Step 1: Group row IDs by "Code" (calendar names)
        calendar_name_to_ids = self.db.index_non_unique(table_name="HolidayCalendar", field_name="Code")

        # Step 2: Iterate over each calendar name and fetch holiday dates
        for calendar_name, row_ids in calendar_name_to_ids.items():
            holiday_dates = []

            for row_id in row_ids:
                # Fetch the DataRow for the given row_id
                data_row = self.db.get_data_row(table_name="HolidayCalendar", row_id=row_id)

                # Extract the "Date" field from the row
                holiday_date = data_row.get_data_field("Date").get_local_date()
                holiday_dates.append(holiday_date)

            # Create the HolidayCalendar object
            calendar_id = HolidayCalendarId.of(calendar_name)
            calendar = ImmutableHolidayCalendar.of(calendar_id, holiday_dates, self.get_weekend_list(None))

            # Add the calendar to the map
            self.calendar_map[calendar_name] = calendar


