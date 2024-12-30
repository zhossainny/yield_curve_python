from yield_curve.common.curve.CurveInterpolator import CurveInterpolator, CurveException


class FlatForwardInterpolator(CurveInterpolator):
    def __init__(self, curve):
        """
        Initialize the FlatForwardInterpolator with a Curve instance.
        :param curve: Instance of a class implementing the Curve interface.
        """
        self.curve = curve
        self.x = None
        self.y = None
        self.rt = None

    def initialize(self):
        """
        Prepare any transformations or setup required for interpolation.
        This method initializes x, y, and rt arrays based on the given curve.
        """
        self.x = self.curve.get_x()
        self.y = self.curve.get_y()
        self.rt = [0] * len(self.x)

        for i in range(len(self.x)):
            t = self.x[i] - self.x[0]
            self.rt[i] = self.y[i] * t

    def interpolate(self, low_index: int, ax: float) -> float:
        """
        Interpolate a value using the flat forward method.
        :param low_index: The lower index for interpolation.
        :param ax: The value to interpolate.
        :return: Interpolated value as a float.
        :raises CurveException: If the value is not bracketed.
        """
        x1 = self.x[low_index]
        x2 = self.x[low_index + 1]
        y1 = self.rt[low_index]
        y2 = self.rt[low_index + 1]
        t = ax - self.x[0]

        # Special case when t == 0
        if t == 0:
            return self.y[0]

        # Ensure ax is within the range [x1, x2]
        if not (x1 <= ax <= x2):
            raise CurveException("Not bracketed")

        ay = y1 + (ax - x1) * ((y2 - y1) / (x2 - x1))
        return ay / t
