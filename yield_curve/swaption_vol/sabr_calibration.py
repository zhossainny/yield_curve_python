import numpy as np
from scipy.optimize import minimize
from typing import List, Tuple

from yield_curve.swaption_vol.sabr import Sabr
from yield_curve.swaption_vol.sabr_params import SabrParams
from yield_curve.swaption_vol.smile import Smile


class PointValuePair:
    """Represents the result of an optimization with its point and value."""

    def __init__(self, point: List[float], value: float):
        self.point = point
        self.value = value


class SabrCalibration:
    def __init__(self, smile: Smile, beta: float):
        self.smile = smile
        self.calib_params = SabrParams(0.5, beta, 0.5, 0.5)
        self.alpha_method = "POWELL"  # Ignoring Brent as requested

    from scipy.optimize import minimize

    def solve_alpha(self, params: SabrParams,  smile: Smile) -> SabrParams:
        """
        Solve for the alpha parameter using Powell's method.
        :param smile:
        :param params: Current SABR parameters.
        :param atm_fwd: ATM forward price.
        :param atm_vol: ATM volatility.
        :return: Updated SABR parameters with calibrated alpha.
        """

        def alpha_objective(alpha: float) -> float:
            params.set_alpha(alpha)
            x = ((1.0 - params.get_beta() * params.get_beta()) * smile.get_expiry_time())/(24*pow(smile.atm_fwd,(2.0-2.0 * params.get_beta())))

            x = x * alpha + (params.get_rho()*params.get_beta()*params.get_nu()*smile.get_expiry_time()) / (4.0 * pow(smile.atm_fwd,(1.0-params.get_beta())))
            x = x * alpha + 1.0 + ((2.0 - 3.0*params.get_rho()*params.get_rho())/24.0) * params.get_nu()*params.get_nu()*smile.get_expiry_time()
            x = x * alpha - smile.atm_vol * pow(smile.atm_fwd, 1.0 - params.get_beta())
            return x

        # Initial guess for alpha
        initial_alpha = smile.atm_vol * pow(smile.atm_fwd, 1.0 - params.get_beta())

        # Perform optimization using Powell's method
        options = {
            'xtol': 1e-4,
            'ftol': 1e-4,
            'maxiter': 100,
            'disp': True
        }
        bounds = [(0, 10)]
        result = minimize(
            alpha_objective,
            x0=initial_alpha,
            method='Powell',
            bounds=bounds,
            options=options
        )

        # Set the optimized alpha
        params.set_alpha(result.x[0])
        return params

    def grid_search(self, problem) -> Tuple[float, float]:
        best_guess = [0.5, 0.5]
        min_error = float("inf")

        for i in range(10):
            for j in range(10):
                guess = [i / 9.0, j / 9.0]
                error = problem.value(guess)
                if error < min_error:
                    min_error = error
                    best_guess = guess

        return best_guess

    def calibrate(self) -> SabrParams:
        problem = SabrProblem(self.smile, self.calib_params)
        guess = self.grid_search(problem)

        result = minimize(
            problem.value,
            x0=guess,
            bounds=[(0.0, 1.0), (-1.0, 1.0)],
            method="Powell",
            options={"ftol": 1e-12, "xtol": 1e-18, "maxiter": 2000},
        )

        params = SabrParams(0.000001, self.calib_params.get_beta(), result.x[0], result.x[1])
        params = self.solve_alpha(params, self.smile)
        return params


class SabrProblem:
    def __init__(self, smile: Smile, calib_params: SabrParams):
        self.smile = smile
        self.calib_params = calib_params

    def value(self, nu_and_rho: List[float]) -> float:
        try:
            params = SabrParams(0.000001, self.calib_params.get_beta(), nu_and_rho[0], nu_and_rho[1])
            params = SabrCalibration.solve_alpha(
                SabrCalibration, params, self.smile
            )
        except Exception:
            return 5.0  # Fallback error

        error = 0.0
        for strike, vol in zip(self.smile.get_strikes(), self.smile.get_vols()):
            calc_vol = Sabr.sabr_volatility(strike, self.smile.get_atm_fwd(), self.smile.get_expiry_time(), params.alpha, params.beta, params.nu, params.rho)
            error += (calc_vol - vol) ** 2
        return error
