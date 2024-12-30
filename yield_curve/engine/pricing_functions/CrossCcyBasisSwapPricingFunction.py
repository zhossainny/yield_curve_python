from typing import List, Optional
from datetime import date
import math
import numpy as np

from yield_curve.engine.calib_instrument.calibration_context import CalibrationContext
from yield_curve.engine.curve_adjustment.curve_adjuster import CurveAdjuster
from yield_curve.engine.date.business_day_convention import BusinessDayConvention
from yield_curve.engine.date.abs_holiday_calendar import HolidayCalendar
from yield_curve.engine.date.day_count import DayCount


# ToDo TEST IT. Formula has been set, same approach as other swap type, but has not been tested
class CrossCcyBasisSwapPricingFunction:
    def __init__(self, ctx: CalibrationContext, value_date: date, settle_date: date,
                 a_float_index_id: int, a_day_count_cd: str, b_float_index_id: int,
                 reset_frequency_cd: str, business_day_cd: str, spread_on_base_leg: bool,
                 fixed_notionals_on_base_leg: bool, principal_adjust_at_each_cf: bool,
                 calendar_cd: str, quoted_spread: float, fx_context):
        self.ctx = ctx
        self.value_date = value_date
        self.settle_date = settle_date
        self.spread_on_base_leg = spread_on_base_leg
        self.fixed_notionals_on_base_leg = fixed_notionals_on_base_leg
        self.principal_adjust_at_each_cf = principal_adjust_at_each_cf
        self.quoted_spread = quoted_spread
        self.fx_context = fx_context

        # Retrieve index data
        self.a_float_index_data = ctx.get_float_index_data(a_float_index_id)
        self.a_float_index_cd = self.a_float_index_data["Code"]

        self.b_float_index_data = ctx.get_float_index_data(b_float_index_id)
        self.b_float_index_cd = self.b_float_index_data["Code"]

        # Retrieve calendar data
        holiday_calendar_id = ctx.get_holiday_calendar_id(calendar_cd)
        self.calendar = ctx.get_calendar(holiday_calendar_id)

        # Calculate maturity date
        self.maturity_date = BusinessDayConvention.of(business_day_cd).adjust(
            self.settle_date + ctx.get_period(reset_frequency_cd), self.calendar
        )

        # Generate schedules and accrual factors
        self.reset_dates, self.a_accrual_factors = self.gen_schedule(
            self.settle_date, self.maturity_date, reset_frequency_cd, business_day_cd, a_day_count_cd
        )
        self.b_accrual_factors = self.gen_schedule(
            self.settle_date, self.maturity_date, reset_frequency_cd, business_day_cd, a_day_count_cd
        )[1]

        self.base_discount_factors = None  # Placeholder for discount factors

    def gen_schedule(self, start_date: date, end_date: date, frequency_cd: str,
                     business_day_cd: str, day_count_cd: str):
        """
        Generates payment schedules and accrual factors.
        """
        day_count = DayCount.of(day_count_cd)
        business_day_convention = BusinessDayConvention.of(business_day_cd)

        # Generate periodic schedule
        periods = []  # List of start-end date tuples
        current_date = start_date
        while current_date < end_date:
            next_date = current_date + self.ctx.get_period(frequency_cd)
            next_date = business_day_convention.adjust(next_date, self.calendar)
            periods.append((current_date, next_date))
            current_date = next_date

        # Generate accrual factors
        accrual_factors = [
            day_count.year_fraction(start, end) for start, end in periods
        ]

        return [end for _, end in periods], accrual_factors

    def calc_fx_forwards(self, target_discount_factors: List[float]) -> List[float]:
        """
        Calculates FX forwards using target discount factors.
        """
        fx_forwards = [0] * len(target_discount_factors)
        fx_spot = self.fx_context.get_fx_spot()

        for i in range(1, len(target_discount_factors)):
            fx_forwards[i] = fx_spot * self.base_discount_factors[i] / target_discount_factors[i]

        return fx_forwards

    def calc_base_notionals(self, fx_forwards: List[float]) -> List[float]:
        """
        Calculates base leg notionals.
        """
        notionals = [1.0 / f if self.fixed_notionals_on_base_leg else f for f in fx_forwards]

        if self.principal_adjust_at_each_cf:
            for i in range(1, len(notionals)):
                notionals[i] = notionals[i - 1]

        return notionals

    def calc_leg_pv(self, notionals: List[float], fixing_rates: List[float], accrual_factors: List[float],
                    reset_dates: List[float], discount_factors: List[float]) -> float:
        """
        Calculates present value of a leg.
        """
        pv = 0.0
        for i in range(len(reset_dates)):
            rate = fixing_rates[i]
            accrual = notionals[i] * rate * accrual_factors[i]
            pv += accrual * discount_factors[i]

        return pv

    def value(self, adjuster: CurveAdjuster) -> float:
        """
        Calculates the value of the cross-currency basis swap.
        """
        # Assign curves
        a_curve = adjuster.get_projection_curve(self.a_float_index_cd)
        b_curve = adjuster.get_projection_curve(self.b_float_index_cd)
        discount_curve = adjuster.get_discount_curve()

        # Calculate discount factors
        if self.base_discount_factors is None:
            self.base_discount_factors = self.calc_fx_forwards(discount_curve.interpolate(self.reset_dates))

        fx_forwards = self.calc_fx_forwards(discount_curve.interpolate(self.reset_dates))
        a_notionals = self.calc_base_notionals(fx_forwards)
        b_notionals = self.calc_base_notionals(fx_forwards)

        # Calculate present values
        a_pv = self.calc_leg_pv(a_notionals, [0] * len(self.reset_dates), self.a_accrual_factors,
                                self.reset_dates, discount_curve.interpolate(self.reset_dates))
        b_pv = self.calc_leg_pv(b_notionals, [0] * len(self.reset_dates), self.b_accrual_factors,
                                self.reset_dates, discount_curve.interpolate(self.reset_dates))

        return b_pv - a_pv
