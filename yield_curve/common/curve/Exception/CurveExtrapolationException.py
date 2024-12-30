from yield_curve.common.curve.Exception.CurveException import CurveException


class CurveExtrapolationException(CurveException):
    """
    Exception class for errors related to curve extrapolation.
    Inherits from CurveException.
    """

    def __init__(self, msg=None, cause=None):
        """
        Initialize the CurveExtrapolationException.
        :param msg: Error message (str).
        :param cause: Original exception (optional).
        """
        super().__init__(msg, cause)
