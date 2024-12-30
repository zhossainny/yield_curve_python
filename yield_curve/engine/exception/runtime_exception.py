class EngineRuntimeException(RuntimeError):
    def __init__(self, msg: str = "", cause: Exception = None):
        super().__init__(msg)
        self.cause = cause
