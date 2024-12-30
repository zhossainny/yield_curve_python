from yield_curve.common.curve.Exception.EngineException import EngineException


class ConvergenceException(EngineException):
    def __init__(self, msg: str = "", cause: Exception = None):
        super().__init__(msg)
        self.cause = cause
