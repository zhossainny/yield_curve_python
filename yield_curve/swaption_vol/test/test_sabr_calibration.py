import unittest
import numpy as np
from math import isclose

from yield_curve.swaption_vol.sabr import Sabr
from yield_curve.swaption_vol.sabr_calibration import SabrCalibration
from yield_curve.swaption_vol.smile import Smile


class TestSabrCalibration(unittest.TestCase):

    def test_sabr_2x5_example(self):
        # Define strikes and forward
        strikes = np.array([-150, -100, -50, -25, 0, 25, 50, 100, 150])
        forward = 0.030721124202973293
        beta = 0.5

        # Adjust strikes to absolute values
        strikes = forward + strikes / 10000.0

        # Define volatilities
        vols = np.array([47.05, 41.29, 37.78, 36.72, 36.04, 35.67, 35.55, 35.83, 36.5])
        vols = vols / 100.0  # Convert to decimals

        # Time to expiry
        t_exp = 2.0027397260273974

        # Create Smile object
        smile = Smile(vols.tolist(), strikes.tolist(), strikes[4], vols[4], t_exp)

        # Create SABR Calibration
        calibrator = SabrCalibration(smile, beta)
        params = calibrator.calibrate()

        # Assertions
        # Uncomment to see intermediate values in the debug console
        # print("Calibrated SABR Parameters:")
        # print(params)
        # print("Errors:")

        sum_err = 0.0
        for i in range(len(strikes)):
            calc_vol = Sabr.sabr_volatility(strikes[i], smile.get_atm_fwd(), smile.get_expiry_time(), params)
            err = calc_vol - vols[i]
            sum_err += err * err

            # Uncomment to see individual errors
            # print(f"Strike: {strikes[i]:.6f}, CalcVol: {calc_vol:.6f}, Error: {err:.6f}")

        # Print the total error if needed
        # print(f"Sum squared error: {sum_err}")

        # Check the sum squared error within tolerance
        self.assertTrue(sum_err < 2e-5, "Sum squared error exceeds tolerance")

        # Check the calibrated parameters
        self.assertTrue(isclose(params.get_alpha(), 0.0519278, rel_tol=1e-6), "Alpha parameter mismatch")
        self.assertTrue(isclose(params.get_beta(), 0.5, rel_tol=1e-6), "Beta parameter mismatch")
        self.assertTrue(isclose(params.get_nu(), 2.2673859871671976, rel_tol=1e-12), "Nu parameter mismatch")
        self.assertTrue(isclose(params.get_rho(), 0.5, rel_tol=1e-6), "Rho parameter mismatch")


# Uncomment the following lines to run the test manually
# if __name__ == "__main__":
#     unittest.main()
