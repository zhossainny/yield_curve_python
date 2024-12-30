from yield_curve.common.curve.Exception.EngineException import EngineException


class CurveException(EngineException):
    """
    Exception class for errors related to curves.
    Inherits from the base Exception class in Python.
    """

    def __init__(self, msg=None, cause=None):
        """
        Initialize the CurveException.
        :param msg: Error message (str).
        :param cause: Original exception (optional).
        """
        super().__init__(msg)
        self.cause = cause
