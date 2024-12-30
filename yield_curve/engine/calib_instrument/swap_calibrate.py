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

import math
from typing import List, Dict, Optional
from datetime import datetime, date

from yield_curve.common.curve.Exception.EngineException import EngineException
from yield_curve.engine.calib_instrument.calibration_context import CalibrationContext
from yield_curve.engine.calib_instrument.quote import Quote
from yield_curve.engine.pricing_functions.SwapPricingFunction import SwapPricingFunction
from yield_curve.engine.pricing_functions.abs_pricing_function import PricingFunction


class Period:
    def getYears(self) -> int:
        pass

    def getMonths(self) -> int:
        pass


class InstrumentType:
    SWAP = "SWAP"

class Map(Dict):
    pass


class CalibInstrument:
    def __init__(self, settlement_lag: int, settlement_calendar_cd: str):
        self.settlement_lag = settlement_lag
        self.settlement_calendar_cd = settlement_calendar_cd


class CalibSwap(CalibInstrument):
    def __init__(self, id: int, ticker: str, settlement_lag: int, settlement_calendar_cd: str,
                 float_index_id: int, tenor: Period,
                 fixed_freq_cd: str, fixed_day_count_cd: str, fixed_business_day_cd: str,
                 float_freq_cd: str, float_day_count_cd: str, float_business_day_cd: str):
        super().__init__(settlement_lag, settlement_calendar_cd)
        self.id: int = id
        self.ticker: str = ticker
        self.float_index_id: int = float_index_id
        self.tenor: Period = tenor
        self.fixed_freq_cd: str = fixed_freq_cd
        self.fixed_day_count_cd: str = fixed_day_count_cd
        self.fixed_business_day_cd: str = fixed_business_day_cd
        self.float_freq_cd: str = float_freq_cd
        self.float_day_count_cd: str = float_day_count_cd
        self.float_business_day_cd: str = float_business_day_cd

    def getFloatIndexID(self) -> int:
        return self.float_index_id

    def getInstrumentType(self) -> str:
        return InstrumentType.SWAP

    def getTenor(self) -> Period:
        return self.tenor

    def getTicker(self) -> str:
        return self.ticker

    def getOrder(self) -> float:
        return float(self.tenor.getYears() + self.tenor.getMonths() / 12.0)

    def getID(self) -> int:
        return self.id

    def getSwapRate(self, quote_map: Dict[int, List[Quote]]) -> float:
        price: float = float('nan')
        quote_list: Optional[List[Quote]] = quote_map.get(self.getID())

        if quote_list is None:
            raise EngineException(f"Missing quotes for swap {self.getID()}")

        for q in quote_list:
            if q.getField() == Quote.QuoteField.PRICE:
                price = q.getValue()

        if math.isnan(price):
            raise EngineException(f"Missing price for swap {self.getID()}")

        return price

    def resolve(self, ctx: CalibrationContext, value_date: date,
                quote_map: Dict[int, List[Quote]]) -> PricingFunction:
        price = self.getSwapRate(quote_map)

        return SwapPricingFunction(
            ctx=ctx,
            value_date=value_date,
            settle_date=self.getSettleDate(ctx, value_date),
            float_index_id=self.float_index_id,
            tenor=self.tenor,
            fixed_freq_cd=self.fixed_freq_cd,
            fixed_day_count_cd=self.fixed_day_count_cd,
            fixed_business_day_cd=self.fixed_business_day_cd,
            float_freq_cd=self.float_freq_cd,
            float_day_count_cd=self.float_day_count_cd,
            float_business_day_cd=self.float_business_day_cd,
            calendar_cd=self.settlement_calendar_cd,
            target_rate=price
        )

    def getSettleDate(self, ctx: CalibrationContext, value_date: date) -> date:
        # Placeholder for calculating the settle date
        return value_date


