class InterpolationMethod:
    """
    Represents various interpolation methods with associated codes.
    """
    LINEAR_DF = "LDF"
    LINEAR_ZERO = "LZ"
    FLAT_FORWARD = "FF"
    CUBIC_SPLINE = "CS"
    MONOTONE_CONVEX = "MC"

    _codes = {
        LINEAR_DF: "LDF",
        LINEAR_ZERO: "LZ",
        FLAT_FORWARD: "FF",
        CUBIC_SPLINE: "CS",
        MONOTONE_CONVEX: "MC",
    }

    @classmethod
    def from_code(cls, code):
        """
        Get the interpolation method corresponding to the given code.
        :param code: Code string for the interpolation method.
        :return: Interpolation method as a string. Defaults to LINEAR_ZERO.
        """
        for method, method_code in cls._codes.items():
            if method_code == code:
                return method
        return cls.LINEAR_ZERO  # Default
