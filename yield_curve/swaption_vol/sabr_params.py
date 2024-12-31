class SabrParams:
    """Class to hold SABR model parameters."""
    def __init__(self, alpha: float, beta: float, nu: float, rho: float):
        self.alpha = alpha
        self.beta = beta
        self.nu = nu
        self.rho = rho

    def get_alpha(self) -> float:
        return self.alpha

    def set_alpha(self, alpha: float):
        self.alpha = alpha

    def get_beta(self) -> float:
        return self.beta

    def set_beta(self, beta: float):
        self.beta = beta

    def get_nu(self) -> float:
        return self.nu

    def set_nu(self, nu: float):
        self.nu = nu

    def get_rho(self) -> float:
        return self.rho

    def set_rho(self, rho: float):
        self.rho = rho

    def __str__(self):
        return f"SabrParams(alpha={self.alpha}, beta={self.beta}, nu={self.nu}, rho={self.rho})"