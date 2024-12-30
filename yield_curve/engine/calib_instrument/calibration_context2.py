from typing import Dict, List, Set, Optional
from datetime import date
from enum import Enum

from yield_curve.engine.date.immutable_holiday_calendar import ImmutableHolidayCalendar


# Placeholder classes and enums
class EngineException(Exception):
    pass


class DayOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class HolidayCalendarId:
    @staticmethod
    def of(name: str) -> str:
        return name  # Use the name as the ID for simplicity


# class ImmutableHolidayCalendar:
#     @staticmethod
#     def of(calendar_id: str, holiday_dates: List[date], weekend_days: List[DayOfWeek]) -> Dict:
#         return {
#             "id": calendar_id,
#             "holidays": holiday_dates,
#             "weekends": weekend_days,
#         }


class DataBase:
    def __init__(self):
        self.tables: Dict[str, Dict[str, List[Dict]]] = {}

    def index_non_unique(self, table_name: str, field_name: str) -> Dict[str, List[int]]:
        if table_name not in self.tables:
            raise ValueError(f"Table {table_name} does not exist")

        table = self.tables[table_name]
        index = {}
        for i, row in enumerate(table):
            key = row.get(field_name)
            if key is not None:
                if key not in index:
                    index[key] = []
                index[key].append(i)
        return index

    def get_data_row(self, table_name: str, row_id: int) -> Dict:
        if table_name not in self.tables:
            raise ValueError(f"Table {table_name} does not exist")

        table = self.tables[table_name]
        if row_id < 0 or row_id >= len(table):
            raise ValueError(f"Row ID {row_id} is out of bounds for table {table_name}")

        return table[row_id]


# CalibrationContext class
class CalibrationContext2:
    def __init__(self, db: DataBase):
        self.db = db
        self.calendar_map: Dict[str, ImmutableHolidayCalendar] = {}
        self.build_calendars()

    def  get_calendar(self, code: str) -> Optional[Dict]:
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
        """
        Build holiday calendars and populate the calendar map.
        """
        # Initialize the calendar map
        self.calendar_map: Dict[str, dict] = {}

        # Group row IDs by "Code" (calendar names)
        calendar_name_to_ids = self.db.index_non_unique(table_name="HolidayCalendar", field_name="Code")

        for calendar_name, row_ids in calendar_name_to_ids.items():
            holiday_dates = []

            for row_id in row_ids:
                # Fetch the row data directly as a dictionary
                data_row = self.db.get_data_row(table_name="HolidayCalendar", row_id=row_id)
                holiday_date = data_row.get("Date")
                if isinstance(holiday_date, date):
                    holiday_dates.append(holiday_date)

            # Create an ImmutableHolidayCalendar object
            calendar_id = calendar_name
            weekend_days = {5, 6}  # Default weekend days: Saturday (5) and Sunday (6)
            calendar = ImmutableHolidayCalendar(calendar_id, holiday_dates, weekend_days)

            # Store the calendar as a dictionary
            self.calendar_map[calendar_name] = calendar.to_dict()

