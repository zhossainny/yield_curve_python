from typing import List, Optional
from abc import ABC, abstractmethod

import numpy as np

from yield_curve.common.curve.Curve import Curve
from yield_curve.common.curve.CurveImp import CurveImpl
from yield_curve.common.curve.Exception.EngineException import EngineException
from yield_curve.common.curve.InterpolationMethod import InterpolationMethod
from yield_curve.engine.curve_adjustment.curve_adjuster_parameters import CurveAdjusterParams
from yield_curve.engine.exception.coonvergence_exception import ConvergenceException


class CurveAdjuster:
    """Python translation of the CurveAdjuster class."""

    class StubType:
        FLAT = "FLAT"
        LINEAR = "LINEAR"

    def __init__(self, valuation_date: float, curve_max_date: float,
                 initial_anchor_curve: Curve, initial_basis_curve: Curve,
                 input_discount_curve: Optional[Curve], anchor_is_discount: bool,
                 anchor_params: CurveAdjusterParams, basis_params: CurveAdjusterParams):
        self.basis_mid_long_basis_y = None
        self.basis_short_mid_basis_y = None
        self.diff_curve_y = None
        self.anchor_mid_long_basis_y = None
        self.anchor_short_mid_basis_y = None
        self.anchor_curve_y = None
        self.basis_curve = None
        self.valuation_date = valuation_date
        self.curve_max_date = curve_max_date
        self.input_discount_curve = input_discount_curve
        self.anchor_is_discount = anchor_is_discount
        self.anchor_params = anchor_params
        self.basis_params = basis_params
        self.stub_type = CurveAdjuster.StubType.FLAT

        # Build curves for the anchor and basis
        anchor_curves = self.build_curves(initial_anchor_curve, anchor_params)
        self.anchor_curve = anchor_curves[0]
        self.anchor_short_mid_basis = anchor_curves[1]
        self.anchor_mid_long_basis = anchor_curves[2]

        basis_curves = self.build_curves(self.curve_diff(initial_basis_curve, initial_anchor_curve), basis_params)
        self.diff_curve = basis_curves[0]
        self.basis_short_mid_basis = basis_curves[1]
        self.basis_mid_long_basis = basis_curves[2]

        # Initialize backup arrays for restoring
        self.anchor_curve_y = np.copy(self.anchor_curve.get_y())
        self.anchor_short_mid_basis_y = np.copy(self.anchor_short_mid_basis.get_y())
        self.anchor_mid_long_basis_y = np.copy(self.anchor_mid_long_basis.get_y())

        self.diff_curve_y = np.copy(self.diff_curve.get_y())
        self.basis_short_mid_basis_y = np.copy(self.basis_short_mid_basis.get_y())
        self.basis_mid_long_basis_y = np.copy(self.basis_mid_long_basis.get_y())

        # Update basis curve
        self.update_basis_curve()

    def update_anchor_curve(self, initial_anchor_curve: Curve):
        # Check if there are calibration instruments against the anchor curve
        if self.anchor_params.get_num_total_points() != 0:
            raise EngineException("Cannot update anchor curve when there are calibration instruments against it.")

        # Reinitialize with the new input anchor curve
        if len(self.anchor_curve.get_x()) != len(initial_anchor_curve.get_x()):
            raise EngineException("Cannot change the number of points on the anchor curve.")

        for i in range(len(self.anchor_curve.get_x())):
            if self.anchor_curve.get_x()[i] != initial_anchor_curve.get_x()[i]:
                raise EngineException("Cannot change dates on the anchor curve.")

        # Copy the new values from the initialAnchorCurve to anchorCurve
        np.copyto(self.anchor_curve.get_y(), initial_anchor_curve.get_y())
        self.anchor_curve.update()

    def restore_curves(self):
        # Restore anchor curve and its basis curves
        np.copyto(self.anchor_curve.get_y(), self.anchor_curve_y)
        np.copyto(self.anchor_short_mid_basis.get_y(), self.anchor_short_mid_basis_y)
        np.copyto(self.anchor_mid_long_basis.get_y(), self.anchor_mid_long_basis_y)

        # Restore diff curve and its basis curves
        np.copyto(self.diff_curve.get_y(), self.diff_curve_y)
        np.copyto(self.basis_short_mid_basis.get_y(), self.basis_short_mid_basis_y)
        np.copyto(self.basis_mid_long_basis.get_y(), self.basis_mid_long_basis_y)

    def build_curves(self, initial_curve: Curve, params: CurveAdjusterParams) -> List[CurveImpl]:
        curve_dates = params.get_curve_dates(self.valuation_date, self.curve_max_date)
        # ToDo
        curve_dates = [date for date in curve_dates if date != 0]
        curve_rates = np.zeros(len(curve_dates))  # Initialize with zeros

        result = [CurveImpl] * 3  # Predefine a list for 3 CurveImpl instances

        # Special case: no curve points
        if len(curve_dates) == 2:
            # Copy the input curve
            result[0] = CurveImpl(
                np.array(initial_curve.get_x()),
                np.array(initial_curve.get_y()),
                params.get_interpolation_method()
            )
            if params == self.basis_params:
                # For a basis curve, mark it as flat
                result[0] = CurveImpl(
                    np.array([self.valuation_date, self.curve_max_date]),
                    np.array([0.0, 0.0]),
                    InterpolationMethod.LINEAR_ZERO
                )
                result[1] = CurveImpl(
                    np.array([self.valuation_date, self.curve_max_date]),
                    np.array([0.0, 0.0]),
                    InterpolationMethod.LINEAR_ZERO
                )
                result[2] = CurveImpl(
                    np.array([self.valuation_date, self.curve_max_date]),
                    np.array([0.0, 0.0]),
                    InterpolationMethod.LINEAR_ZERO
                )
            return result

        # Fill curve_rates for intermediate dates
        for i in range(1, len(curve_dates) - 1):
            curve_rates[i] = initial_curve.interpolate(curve_dates[i])

        # Plug in a rate for t=0
        curve_rates[0] = curve_rates[1]

        # Handle extrapolation for the last rate
        if params.get_long_dates() and params.get_long_dates()[-1] == self.curve_max_date:
            curve_rates[-1] = initial_curve.interpolate(curve_dates[-1])
        else:
            self.extrapolate(curve_dates, curve_rates, params)

        # Create the primary curve
        result[0] = CurveImpl(
            np.array(curve_dates),
            np.array(curve_rates),
            params.get_interpolation_method()
        )

        # Handle overlaps
        overlap_dates = params.get_short_mid_overlap_dates(self.valuation_date)
        overlap_rates = np.zeros(len(overlap_dates))
        result[1] = CurveImpl(
            np.array(overlap_dates),
            np.array(overlap_rates),
            InterpolationMethod.LINEAR_ZERO
        )

        overlap_dates = params.get_mid_long_overlap_dates(self.valuation_date)
        overlap_rates = np.zeros(len(overlap_dates))
        result[2] = CurveImpl(
            np.array(overlap_dates),
            np.array(overlap_rates),
            InterpolationMethod.LINEAR_ZERO
        )

        return result

    def curve_diff(self, a: Curve, b: Curve) -> CurveImpl:
        curve_dates = np.copy(a.get_x())
        curve_rates = np.zeros(len(curve_dates))
        for i in range(len(curve_dates)):
            curve_rates[i] = b.interpolate(curve_dates[i]) - a.get_y()[i]
        return CurveImpl(curve_dates,curve_rates, InterpolationMethod.LINEAR_DF)

    def update_basis_curve(self):
        # The basis curve is a curve that is anchor + diff on the nodes of the anchor
        curve_dates = np.copy(self.anchor_curve.get_x())  # Copy the X values of anchorCurve
        curve_rates = np.zeros(len(curve_dates))  # Initialize curveRates with zeros

        diff_max_date = self.diff_curve.get_x()[-1]
        diff_max_rate = self.diff_curve.get_y()[-1]

        # Calculate curve rates based on anchorCurve and diffCurve
        for i, date in enumerate(curve_dates):
            if date > diff_max_date:
                curve_rates[i] = self.anchor_curve.get_y()[i] + diff_max_rate
            else:
                curve_rates[i] = self.anchor_curve.get_y()[i] + self.diff_curve.interpolate(date)

        # Check if basisCurve needs to be created or updated
        if self.basis_curve is None or len(self.basis_curve.get_x()) != len(curve_dates):
            self.basis_curve = CurveImpl(
                np.array(curve_dates),
                np.array(curve_rates),
                self.basis_params.get_interpolation_method()
            )
        else:
            # Update existing basisCurve
            np.copyto(self.basis_curve.get_x(), np.array(curve_dates))
            np.copyto(self.basis_curve.get_y(), np.array(curve_rates))
            self.basis_curve.update()

    def extrapolate(self, curve_dates: np.ndarray, curve_rates: np.ndarray, params: CurveAdjusterParams):
        if len(params.get_long_dates()) == 0 or params.get_long_dates()[-1] == self.curve_max_date:
            return
        else:
            i = len(curve_rates) - 3
            if i >= 0:
                # Flat forward extrapolation
                t1 = curve_dates[i] / 365.0
                t2 = curve_dates[i + 1] / 365.0
                t3 = curve_dates[i + 2] / 365.0

                fwd = ((curve_rates[i + 1] * t2) - (curve_rates[i] * t1)) / (t2 - t1)

                curve_rates[i + 2] = (curve_rates[i + 1] * t2 + fwd * (t3 - t2)) / t3
            else:
                curve_rates[-1] = curve_rates[-2]

    def extrapolate_diff(self, curve_rates: np.ndarray, params: CurveAdjusterParams):
        if len(params.get_long_dates()) == 0 or params.get_long_dates()[-1] == self.curve_max_date:
            return
        else:
            # Flat extrapolation
            curve_rates[-1] = curve_rates[-2]

    def set_stub_rate(self, stub_type: str):
        if stub_type == CurveAdjuster.StubType.FLAT:
            self.anchor_curve.get_y()[0] = self.anchor_curve.get_y()[1]
        else:
            x1, x2 = self.anchor_curve.get_x()[:2]
            y1, y2 = self.anchor_curve.get_y()[:2]
            slope = (y2 - y1) / (x2 - x1)
            self.anchor_curve.get_y()[0] = y1 - slope * (x1 - self.anchor_curve.get_x()[0])

    def merge_nodes(self, a_nodes: np.ndarray, b_nodes: np.ndarray) -> np.ndarray:
        merged = np.zeros(len(a_nodes) + len(b_nodes))
        merged_idx = 0
        call_idx = 0
        cpn_idx = 0

        while call_idx < len(b_nodes) or cpn_idx < len(a_nodes):
            if call_idx == len(b_nodes) or (cpn_idx < len(a_nodes) and (b_nodes[call_idx] - a_nodes[cpn_idx]) > 0.5):
                # `a_nodes` before `b_nodes`
                merged[merged_idx] = a_nodes[cpn_idx]
                cpn_idx += 1
            elif cpn_idx == len(a_nodes) or (call_idx < len(b_nodes) and (a_nodes[cpn_idx] - b_nodes[call_idx]) > 0.5):
                # `b_nodes` before `a_nodes`
                merged[merged_idx] = b_nodes[call_idx]
                call_idx += 1
            else:
                # Equal within tolerance
                merged[merged_idx] = a_nodes[cpn_idx]
                cpn_idx += 1
                call_idx += 1

            merged_idx += 1

        # Resize the merged array to the actual number of elements
        return merged[:merged_idx]

    def update_high_res_basis_curve(self):
        nodes = self.merge_nodes(self.diff_curve.get_x(), self.anchor_curve.get_x())
        diff_rates = self.diff_curve.interpolate_array2(nodes)
        rates = self.anchor_curve.interpolate_array2(nodes)

        # Add diffRates to rates
        for i in range(len(rates)):
            rates[i] += diff_rates[i]

        if self.high_res_basis_curve is None or len(self.high_res_basis_curve.get_x()) != len(nodes):
            self.high_res_basis_curve = CurveImpl(
                np.array(nodes),
                np.array(rates),
                self.basis_params.get_interpolation_method()
            )
        else:
            # Copy data into existing curve
            np.copyto(self.high_res_basis_curve.get_x(), np.array(nodes))
            np.copyto(self.high_res_basis_curve.get_y(), np.array(rates))
            self.high_res_basis_curve.update()

    def adjust_curves(self, adj_vect: np.ndarray):
        # Put curves back to initial conditions
        self.restore_curves()

        # Check for convergence failures
        num_anchor_pts = self.anchor_params.get_num_total_points()
        for i in range(num_anchor_pts):
            if np.isnan(adj_vect[i]) or adj_vect[i] == float('inf') or adj_vect[i] == float('-inf'):
                raise ConvergenceException(
                    f"Convergence failure on anchor curve index {self.anchor_params.get_index()}"
                )

        for i in range(num_anchor_pts, len(adj_vect)):
            if np.isnan(adj_vect[i]) or adj_vect[i] == float('inf') or adj_vect[i] == float('-inf'):
                raise ConvergenceException(
                    f"Convergence failure on basis curve index {self.basis_params.get_index()}"
                )

        # Adjustments for anchor curve instruments in increasing maturity
        i = 0  # Index into anchor curve
        k = 0  # Index into adj_vect
        if self.anchor_params.get_num_total_points() != 0:
            n_overlap = self.anchor_params.get_num_short_mid_overlap_points()
            for i in range(len(self.anchor_params.get_short_dates()) - n_overlap):
                self.anchor_curve.get_y()[i + 1] += adj_vect[k]
                k += 1

            self.set_stub_rate()

            for i in range(len(self.anchor_params.get_mid_dates()) - n_overlap):
                self.anchor_curve.get_y()[i + 1] += adj_vect[k]
                k += 1

            for i in range(len(self.anchor_params.get_long_dates())):
                self.anchor_curve.get_y()[i + 1] += adj_vect[k]
                k += 1

            # Update anchor curves
            self.extrapolate(self.anchor_curve.get_x(), self.anchor_curve.get_y(), self.anchor_params)
            self.anchor_curve.update()
            self.anchor_short_mid_basis.update()
            self.anchor_mid_long_basis.update()

        # Adjustments for basis curve instruments in increasing maturity
        if self.basis_params.get_num_total_points() != 0:
            n_overlap = self.basis_params.get_num_short_mid_overlap_points()
            for i in range(len(self.basis_params.get_short_dates()) - n_overlap):
                self.basis_short_mid_basis.get_y()[i + 1] += adj_vect[k]
                k += 1

            n_overlap = self.basis_params.get_num_mid_long_overlap_points()
            for i in range(len(self.basis_params.get_mid_dates()) - n_overlap):
                self.basis_mid_long_basis.get_y()[i + 1] += adj_vect[k]
                k += 1

            for i in range(len(self.basis_params.get_long_dates())):
                self.diff_curve.get_y()[i + 1] += adj_vect[k]
                k += 1

            # Set rate at t=0
            self.diff_curve.get_y()[0] = self.diff_curve.get_y()[1]

            # Update basis curves
            self.extrapolate_diff(self.diff_curve.get_y(), self.basis_params)
            self.diff_curve.update()
            self.basis_short_mid_basis.update()
            self.basis_mid_long_basis.update()

        # Update basis curve and high-resolution basis curve
        self.update_basis_curve()
        self.update_high_res_basis_curve()

    def get_discount_curve(self) -> Curve:
        if self.anchor_is_discount:
            return self.anchor_curve
        else:
            return self.basis_curve
