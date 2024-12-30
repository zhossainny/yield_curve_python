class EngineException(Exception):
    """
    Base exception class for engine-related errors.
    Inherits from the built-in Exception class.
    """

    def __init__(self, msg=None, cause=None):
        """
        Initialize the EngineException.
        :param msg: Error message (str).
        :param cause: Original exception (optional).
        """
        super().__init__(msg)
        self.cause = cause
