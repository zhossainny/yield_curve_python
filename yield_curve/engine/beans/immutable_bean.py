from abc import ABC

from yield_curve.engine.beans.bean import Bean


class ImmutableBean(Bean, ABC):
    """
    Represents an ImmutableBean, extending the Bean interface.
    """
    pass
