from typing import List, Optional
from datetime import date

from yield_curve.common.curve.Curve import Curve
from yield_curve.engine.calib_instrument.calibration_context import CalibrationContext
from yield_curve.engine.date.business_day_convention import BusinessDayConvention
from yield_curve.engine.date.immutable_holiday_calendar import ImmutableHolidayCalendar


# ToDo TEST IT. Formula has been set, same approach as other swap type, but has not been tested
class BasisSwapPricingFunction:
    def __init__(
            self,
            ctx: CalibrationContext,
            value_date: date,
            settle_date: date,
            tenor: int,
            a_float_index_cd: str,
            a_reset_freq_cd: str,
            a_payment_freq_cd: str,
            a_day_count_cd: str,
            a_business_day_cd: str,
            b_float_index_cd: str,
            b_reset_freq_cd: str,
            b_payment_freq_cd: str,
            b_day_count_cd: str,
            b_business_day_cd: str,
            calendar_cd: str,
            quoted_spread: float,
    ):
        self.value_date = value_date
        self.settle_date = settle_date
        self.quoted_spread = quoted_spread

        self.a_float_index_data = ctx.get_float_index_id(a_float_index_cd)
        self.b_float_index_data = ctx.get_float_index_id(b_float_index_cd)

        self.calendar = ctx.get_calendar(calendar_cd)

        self.a_accrual_factors = []
        self.b_accrual_factors = []

        self.a_payment_dates = []
        self.b_payment_dates = []

        self._generate_leg_data(
            ctx,
            a_reset_freq_cd,
            a_payment_freq_cd,
            a_day_count_cd,
            a_business_day_cd,
            "a",
        )
        self._generate_leg_data(
            ctx,
            b_reset_freq_cd,
            b_payment_freq_cd,
            b_day_count_cd,
            b_business_day_cd,
            "b",
        )

    def _generate_leg_data(
            self,
            ctx: CalibrationContext,
            reset_freq_cd: str,
            payment_freq_cd: str,
            day_count_cd: str,
            business_day_cd: str,
            leg: str,
    ):
        freq = BusinessDayConvention.from_name(reset_freq_cd)
        day_count = BusinessDayConvention.from_name(day_count_cd)

        if leg == "a":
            schedule = self._create_schedule(
                freq, day_count, self.a_float_index_data, self.settle_date, "a"
            )
            self.a_accrual_factors = schedule["accrual_factors"]
            self.a_payment_dates = schedule["payment_dates"]
        elif leg == "b":
            schedule = self._create_schedule(
                freq, day_count, self.b_float_index_data, self.settle_date, "b"
            )
            self.b_accrual_factors = schedule["accrual_factors"]
            self.b_payment_dates = schedule["payment_dates"]

    def _create_schedule(
            self,
            freq,
            day_count,
            float_index_data,
            settle_date: date,
            leg: str,
    ):
        accrual_factors = []
        payment_dates = []

        start_date = settle_date
        end_date = start_date + freq.to_timedelta()

        while start_date < end_date:
            accrual_factor = day_count.year_fraction(start_date, end_date)
            accrual_factors.append(accrual_factor)
            payment_dates.append(end_date)

            start_date = end_date
            end_date += freq.to_timedelta()

        return {"accrual_factors": accrual_factors, "payment_dates": payment_dates}

    def value(self, adjuster):
        a_curve = adjuster.get_anchor_curve()
        b_curve = adjuster.get_basis_curve()
        discount_curve = adjuster.get_discount_curve()

        a_pv = self._leg_pv(
            self.a_payment_dates,
            self.a_accrual_factors,
            a_curve,
            discount_curve,
            self.quoted_spread,
        )
        b_pv = self._leg_pv(
            self.b_payment_dates,
            self.b_accrual_factors,
            b_curve,
            discount_curve,
            self.quoted_spread,
        )

        return a_pv - b_pv

    def _leg_pv(
            self,
            payment_dates: List[date],
            accrual_factors: List[float],
            curve: Curve,
            discount_curve: Curve,
            spread: float,
    ) -> float:
        pv = 0.0
        for payment_date, accrual_factor in zip(payment_dates, accrual_factors):
            discount_factor = discount_curve.discount(payment_date)
            forward_rate = curve.forward_rate(payment_date)

            cash_flow = (forward_rate + spread) * accrual_factor * discount_factor
            pv += cash_flow

        return pv
