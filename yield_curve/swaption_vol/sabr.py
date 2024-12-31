import math


class Sabr:
    EPSILON = 2.220446049250313e-16

    @staticmethod
    def close(x: float, y: float) -> bool:
        """
        Checks if two numbers are close to each other considering floating point precision.
        """
        if x == y:
            return True
        diff = abs(x - y)
        tolerance = 42 * Sabr.EPSILON
        if x * y == 0.0:
            return diff < tolerance * tolerance
        return diff <= tolerance * abs(x) and diff <= tolerance * abs(y)

    @staticmethod
    def validate_sabr_parameters(alpha: float, beta: float, nu: float, rho: float):
        """
        Validates SABR parameters.
        """
        if alpha <= 0.0:
            raise ValueError(f"alpha must be positive: {alpha}")
        if beta < 0.0 or beta > 1.0:
            raise ValueError(f"beta must be in (0.0, 1.0): {beta}")
        if nu < 0.0:
            raise ValueError(f"nu must be non-negative: {nu}")
        if abs(rho) >= 1.0:
            raise ValueError(f"rho square must be less than one: {rho}")

    @staticmethod
    def sabr_volatility(strike: float, forward: float, expiry_time: float, alpha: float, beta: float, nu: float,
                        rho: float) -> float:
        """
        Calculates SABR volatility using validated SABR parameters.
        """
        Sabr.validate_sabr_parameters(alpha, beta, nu, rho)
        return Sabr.unsafe_sabr_volatility(strike, forward, expiry_time, alpha, beta, nu, rho)

    @staticmethod
    def unsafe_sabr_volatility(strike: float, forward: float, expiry_time: float, alpha: float, beta: float, nu: float,
                               rho: float) -> float:
        """
        SABR volatility implementation without explicit validation.
        """
        one_minus_beta = 1.0 - beta
        A = (forward * strike) ** one_minus_beta
        sqrt_A = math.sqrt(A)
        log_M = 0.0

        if not Sabr.close(forward, strike):
            log_M = math.log(forward / strike)
        else:
            epsilon = forward - strike
            log_M = epsilon / (sqrt_A * alpha)

        z = (nu / alpha) * sqrt_A * log_M
        B = 1.0 - 2.0 * rho * z + z ** 2
        C = one_minus_beta ** 2 * log_M ** 2
        tmp = math.sqrt(B) + z - rho
        xx = (1.0 - rho)
        D = sqrt_A * (1.0 + C / 24.0 + C * C / 1920.0)
        d = (1.0 + expiry_time * (one_minus_beta ** 2 * alpha ** 2) / (24.0 * A) +
             (0.25 * rho * beta * nu * alpha) / sqrt_A +
             (2.0 - 3.0 * rho * rho) * (nu * nu) / 24.0)

        multiplier = 0.0
        m = 10.0

        if abs(z * xx) > Sabr.EPSILON * m:
            multiplier = z / xx
        else:
            multiplier = 1.0 - 0.5 * rho * z - (3.0 * rho ** 2 - 2.0) * z ** 2 / 12.0

        return (alpha / D) * multiplier * d
