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
from typing import Dict
from yield_curve.common.curve.Curve import Curve
from yield_curve.common.curve.curve_implementation import CurveImplementation
from yield_curve.common.model.curve_bundle_abs import CurveBundle


class CurveBundleImplement(CurveBundle):
    """
    Immutable implementation of the CurveBundle interface.
    """

    def __init__(self, curve_bundle: CurveBundle):
        """
        Initialize the CurveBundleImmutable with data from an existing CurveBundle.
        Validates and copies the data to ensure immutability.
        """
        if curve_bundle is None:
            raise ValueError("null curveBundle")

        valuation_date = curve_bundle.get_valuation_date()
        if valuation_date is None:
            raise ValueError("null valuationDate")

        ccy = curve_bundle.get_ccy()
        if ccy is None:
            raise ValueError("null ccy")

        discount_curve = curve_bundle.get_discount_curve()
        if discount_curve is None:
            raise ValueError("null discountCurve")

        csa_discount_curves = curve_bundle.get_csa_discount_curves() or {}
        if any(k is None or v is None for k, v in csa_discount_curves.items()):
            raise ValueError("null csaDiscountCurves key(s) or value(s)")

        projection_curves = curve_bundle.get_projection_curves() or {}
        if any(k is None or v is None for k, v in projection_curves.items()):
            raise ValueError("null projectionCurves key(s) or value(s)")

        projection_fixings = curve_bundle.get_projection_fixings() or {}
        if any(k is None or v is None for k, v in projection_fixings.items()):
            raise ValueError("null projectionFixings key(s) or value(s)")

        fx_spot_rates = curve_bundle.get_fx_spot_rates() or {}
        if any(k is None or v is None for k, v in fx_spot_rates.items()):
            raise ValueError("null fxSpotRates key(s) or value(s)")

        # Copy data to ensure immutability
        self.valuation_date = valuation_date
        self.ccy = ccy
        self.discount_curve = self.to_curve_immutable(discount_curve)
        self.csa_discount_curves = {
            k: self.to_curve_immutable(v) for k, v in csa_discount_curves.items()
        }
        self.projection_curves = {
            k: self.to_curve_immutable(v) for k, v in projection_curves.items()
        }
        self.projection_fixings = dict(projection_fixings)
        self.fx_spot_rates = dict(fx_spot_rates)

    def get_valuation_date(self) -> date:
        """Return the valuation date."""
        return self.valuation_date

    def get_ccy(self) -> str:
        """Return the currency."""
        return self.ccy

    def get_discount_curve(self) -> Curve:
        """Return the discount curve."""
        return self.discount_curve

    def get_projection_curves(self) -> Dict[str, Curve]:
        """Return the projection curves."""
        return self.projection_curves

    def get_csa_discount_curves(self) -> Dict[str, Curve]:
        """Return the CSA discount curves."""
        return self.csa_discount_curves

    def get_projection_curve(self, float_index_cd: str) -> Curve:
        """Return a specific projection curve."""
        return self.projection_curves[float_index_cd]

    def get_projection_fixing(self, float_index_cd: str) -> float:
        """Return a specific projection fixing."""
        return self.projection_fixings[float_index_cd]

    def get_projection_fixings(self) -> Dict[str, float]:
        """Return all projection fixings."""
        return self.projection_fixings

    def get_fx_spot_rates(self) -> Dict[str, float]:
        """Return all FX spot rates."""
        return self.fx_spot_rates

    def __eq__(self, other):
        """Equality check for CurveBundleImmutable."""
        if not isinstance(other, CurveBundleImplement):
            return False

        return (
            self.valuation_date == other.valuation_date
            and self.ccy == other.ccy
            and self.discount_curve == other.discount_curve
            and self.csa_discount_curves == other.csa_discount_curves
            and self.projection_curves == other.projection_curves
            and self.projection_fixings == other.projection_fixings
            and self.fx_spot_rates == other.fx_spot_rates
        )

    def __hash__(self):
        """Generate a hash for CurveBundleImmutable."""
        return hash(
            (
                self.valuation_date,
                self.ccy,
                self.discount_curve,
                frozenset(self.csa_discount_curves.items()),
                frozenset(self.projection_curves.items()),
                frozenset(self.projection_fixings.items()),
                frozenset(self.fx_spot_rates.items()),
            )
        )

    def __str__(self):
        """String representation of CurveBundleImmutable."""
        return (
            f"CurveBundleImmutable("
            f"valuationDate={self.valuation_date}, "
            f"ccy={self.ccy}, "
            f"discountCurve={self.discount_curve}, "
            f"csaDiscountCurves={self.csa_discount_curves}, "
            f"projectionCurves={self.projection_curves}, "
            f"projectionFixings={self.projection_fixings}, "
            f"fxSpotRates={self.fx_spot_rates})"
        )

    @staticmethod
    def to_curve_immutable(curve: Curve) -> CurveImplementation:
        """Convert a Curve to an immutable version if not already immutable."""
        if isinstance(curve, CurveImplementation):
            return curve
        return CurveImplementation(curve)
