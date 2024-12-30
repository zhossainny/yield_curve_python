from datetime import date
from typing import Optional

from yield_curve.common.curve.Curve import Curve
from yield_curve.common.curve.Exception.EngineException import EngineException
from yield_curve.engine.curve_adjustment.curve_adjuster import CurveAdjuster
from yield_curve.engine.calib_instrument.calibration_context import CalibrationContext
from yield_curve.engine.date.business_day_convention import BusinessDayConvention
from yield_curve.engine.date.day_count import DayCount
from yield_curve.engine.date.immutable_holiday_calendar import ImmutableHolidayCalendar


# ToDo TEST IT. Formula has been set, same approach as other swap type, but has not been tested
class FraPricingFunction:
    def __init__(
            self,
            ctx: CalibrationContext,
            value_date: date,
            settle_date: date,
            float_index_id: int,
            tenor: Optional[int],
            business_day_conv: str,
            calendar_cd: str,
            rate: float,
    ):
        # Fetch FloatIndex data
        float_index_data = ctx.get_database().get_data_row("FloatIndex", float_index_id)
        self.float_index_cd = float_index_data.get("Code")
        day_count_str = float_index_data.get("DayCount")
        index_tenor_str = float_index_data.get("Tenor")

        # Initialize DayCount and related dates
        day_count = DayCount.of(day_count_str)
        self.value_date = self.date_to_double(value_date)

        # Handle start and end dates
        start_tenor = tenor
        end_tenor = tenor

        calendar = ctx.get_calendar(calendar_cd)
        business_day_conv = BusinessDayConvention.of(business_day_conv)
        sd = business_day_conv.adjust(settle_date + start_tenor, calendar)
        self.start_date = self.date_to_double(sd)

        ed = business_day_conv.adjust(sd + end_tenor, calendar)
        self.end_date = self.date_to_double(ed)

        self.accrual_factor = day_count.year_fraction(sd, ed)
        self.target_rate = rate

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
        swap_basis = adjuster.get_anchor_short_mid_basis_curve()
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
