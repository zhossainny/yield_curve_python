from typing import List


class Smile:
    """Represents a volatility smile."""

    def __init__(self, vols: List[float], strikes: List[float], atm_fwd: float, atm_vol: float, expiry_time: float):
        self.vols = vols
        self.strikes = strikes
        self.atm_fwd = atm_fwd
        self.atm_vol = atm_vol
        self.expiry_time = expiry_time

    def get_vols(self) -> List[float]:
        return self.vols

    def get_strikes(self) -> List[float]:
        return self.strikes

    def get_atm_fwd(self) -> float:
        return self.atm_fwd

    def get_atm_vol(self) -> float:
        return self.atm_vol

    def get_expiry_time(self) -> float:
        return self.expiry_time
