import numpy as np
from numpy.linalg import LinAlgError

from yield_curve.engine.curve_adjustment.vector_function import VectorFunction
from yield_curve.engine.exception.coonvergence_exception import ConvergenceException


# Equivalent of RealMatrix using NumPy
class RealMatrix:
    def __init__(self, data: np.ndarray):
        self.data = data

    def operate(self, vector: np.ndarray) -> np.ndarray:
        return self.data @ vector

    def add(self, other: 'RealMatrix') -> 'RealMatrix':
        return RealMatrix(self.data + other.data)

    def set_column(self, index: int, column: np.ndarray):
        self.data[:, index] = column


# LU Decomposition using NumPy
class LUDecomposition:
    def __init__(self, matrix: RealMatrix):
        self.lu = np.linalg.inv(matrix.data)  # Compute inverse for solver

    def get_solver(self) -> 'LUSolver':
        return LUSolver(self.lu)


class LUSolver:
    def __init__(self, inverse_matrix: np.ndarray):
        self.inverse_matrix = inverse_matrix

    def solve(self, vector: np.ndarray) -> np.ndarray:
        return self.inverse_matrix @ vector


# QR Decomposition using NumPy
class QRDecomposition:
    def __init__(self, matrix: RealMatrix):
        self.q, self.r = np.linalg.qr(matrix.data)

    def get_q(self) -> RealMatrix:
        return RealMatrix(self.q)


class BroydenSolver:
    def __init__(self, objective: VectorFunction, jacobian: RealMatrix, tolerance: float, bump: float, max_iterations: int):
        """
        Initializes the Broyden solver.
        """
        self.objective = objective
        self.jacobian = jacobian
        self.tolerance = tolerance
        self.bump = bump
        self.max_iter = max_iterations
        self.num_iter = 0

    def build_jacobian(self, x: np.ndarray):
        """
        Builds the Jacobian matrix.
        """
        dim = self.objective.dimension()
        self.jacobian = RealMatrix(np.zeros((dim, dim)))

        base = self.objective.value(x)
        for i in range(dim):
            arg_vect = x.copy()
            arg_vect[i] += self.bump

            result = self.objective.value(arg_vect)
            result = (result - base) / self.bump

            self.jacobian.set_column(i, result)

    def polish_jacobian(self, guess: np.ndarray):
        """
        Polishes the Jacobian matrix using random perturbations.
        """
        dim = self.objective.dimension()
        random_matrix = RealMatrix(np.random.rand(dim, dim))

        qr = QRDecomposition(random_matrix)
        q = qr.get_q()
        random_matrix = q

        f = np.array(self.objective.value(guess))
        f2 = np.array(self.objective.value(guess + self.bump))
        delta_f = f2 - f

        diff = delta_f - self.jacobian.operate(self.bump)
        if np.linalg.norm(diff) < self.bump * 5.0:
            return

        delta_x_norm = np.linalg.norm(self.bump)
        factor = 1.0 / (delta_x_norm ** 2)
        update = diff[:, None] @ self.bump[None, :] * factor
        self.jacobian = self.jacobian.add(RealMatrix(update))

    def solve(self, guess: np.ndarray) -> np.ndarray:
        """
        Solves the problem using the default option to polish the Jacobian matrix.
        """
        return self.solve_with_polish(guess, polish=True)

    def solve_with_polish(self, guess: np.ndarray, polish: bool) -> np.ndarray:
        """
        Solves the problem with the option to polish the Jacobian matrix.
        """
        if self.jacobian is None:
            self.build_jacobian(guess)
        elif polish:
            self.polish_jacobian(guess)

        x = np.array(guess)
        err_vect = self.objective.value(x)
        num_iterations = 0

        while np.linalg.norm(err_vect, ord=np.inf) > self.tolerance:
            lu = LUDecomposition(self.jacobian)
            solver = lu.get_solver()

            delta_x = solver.solve(-err_vect)
            x += delta_x

            next_err_vect = self.objective.value(x)
            delta_f = next_err_vect - err_vect
            diff = delta_f - self.jacobian.operate(delta_x)

            delta_x_norm = np.linalg.norm(delta_x)
            factor = 1.0 / (delta_x_norm ** 2)
            update = diff[:, None] @ delta_x[None, :] * factor
            self.jacobian = self.jacobian.add(RealMatrix(update))

            err_vect = next_err_vect
            num_iterations += 1

            if num_iterations > self.max_iter:
                self.num_iter = num_iterations
                raise ConvergenceException("Maximum number of iterations exceeded")

        self.num_iter = num_iterations
        return x
