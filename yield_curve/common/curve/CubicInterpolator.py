from yield_curve.common.curve.CurveInterpolator import CurveException, CurveInterpolator


class CubicInterpolator(CurveInterpolator):
    def __init__(self, curve):
        """
        Initialize the CubicInterpolator with a Curve instance.
        :param curve: Instance of a class implementing the Curve interface.
        """
        self.curve = curve
        self.x = None
        self.y = None
        self.second_deriv = None

    def initialize(self):
        """
        Prepare any transformations or setup required for cubic interpolation.
        This method initializes the x, y, and second_deriv arrays based on the given curve.
        """
        self.x = self.curve.get_x()
        self.y = self.curve.get_y()
        n = len(self.x)
        self.second_deriv = [0.0] * n
        u = [0.0] * n

        # Forward pass to compute second derivatives
        for i in range(1, n - 1):
            sig = (self.x[i] - self.x[i - 1]) / (self.x[i + 1] - self.x[i - 1])
            p = sig * self.second_deriv[i - 1] + 2.0
            self.second_deriv[i] = (sig - 1.0) / p
            u[i] = (
                (self.y[i + 1] - self.y[i]) / (self.x[i + 1] - self.x[i])
                - (self.y[i] - self.y[i - 1]) / (self.x[i] - self.x[i - 1])
            )
            u[i] = (
                (6.0 * u[i] / (self.x[i + 1] - self.x[i - 1]))
                - sig * u[i - 1]
            ) / p

        # Boundary conditions
        self.second_deriv[0] = 0.0
        self.second_deriv[n - 1] = 0.0

        # Back substitution to finalize second derivatives
        for i in range(n - 2, -1, -1):
            self.second_deriv[i] = self.second_deriv[i] * self.second_deriv[i + 1] + u[i]

    def interpolate(self, low_index: int, ax: float) -> float:
        """
        Interpolate a value using the cubic interpolation method.
        :param low_index: The lower index for interpolation.
        :param ax: The value to interpolate.
        :return: Interpolated value as a float.
        :raises CurveException: If the value is not bracketed or invalid.
        """
        x1 = self.x[low_index]
        x2 = self.x[low_index + 1]
        y1 = self.y[low_index]
        y2 = self.y[low_index + 1]
        sd1 = self.second_deriv[low_index]
        sd2 = self.second_deriv[low_index + 1]

        if not (x1 <= ax <= x2):
            raise CurveException("Not bracketed")

        h = x2 - x1
        if h == 0:
            raise CurveException("X inputs must be distinct")

        a = (x2 - ax) / h
        b = (ax - x1) / h

        # Cubic interpolation formula
        ay = (
            a * y1
            + b * y2
            + ((a ** 3 - a) * sd1 + (b ** 3 - b) * sd2) * (h ** 2) / 6.0
        )
        return ay
