"""
Hessian Update Strategies
-------------------------
This module provides various generic Hessian approximation strategies that
can be employed when the calculating the exact Hessian or an approximation
is computationally too demandind.
"""


from typing import Optional
import numpy as np
from numpy.linalg import norm


class HessianApproximation:
    """
    Abstract class from which Hessian update strategies should subclass
    """
    def __init__(self, hess_init: Optional[np.ndarray] = None):
        """
        Create a Hessian update strategy instance

        :param hess_init:
            Inital guess for the Hessian, if empty Identity matrix will be used
        """
        if hess_init is not None:
            if not isinstance(hess_init, np.ndarray):
                raise ValueError('Cannot initialize with hess_init of type'
                                 f'{type(hess_init)}, needs np.ndarray.')

            if not hess_init.ndim == 2:
                raise ValueError('hess_init needs to be a matrix with'
                                 f'hess_init.ndim == 2, was {hess_init.ndim}')

            if not hess_init.shape[0] == hess_init.shape[1]:
                raise ValueError('hess_init needs to be a square matrix!')

            hess_init = hess_init.copy()

        self.hess_init: np.ndarray = hess_init
        self._hess = None

    def init_mat(self, dim: int):
        """
        Initializes this approximation instance and checks the dimensionality

        :param dim:
            dimension of optimization variables
        """
        if self.hess_init is None:
            self._hess = np.eye(dim)
        else:
            self._hess = self.hess_init.copy()
            if self._hess.shape[0] != dim:
                raise ValueError('Inital approximation had inconsistent '
                                 f'dimension, was {self._hess.shape[0]}, '
                                 f'but should be {dim}.')

    def update(self, s, y):
        raise NotImplementedError()  # pragma : no cover

    def get_mat(self) -> np.ndarray:
        """
        Getter for the Hessian approximation
        :return:
        """
        return self._hess


class SR1(HessianApproximation):
    """
    Symmetric Rank 1 update strategy. This updating strategy may yield
    indefinite hessian approximations.
    """
    def update(self, s, y):
        z = y - self._hess.dot(s)
        d = z.T.dot(s)

        # [NocedalWright2006] (6.26) reject if update degenerate
        if np.abs(d) >= 1e-8 * norm(s) * norm(z):
            self._hess += np.outer(z, z.T)/d


class BFGS(HessianApproximation):
    """
    Broyden-Fletcher-Goldfarb-Shanno update strategy. This is a rank 2
    update strategy that always yields positive-semidefinite hessian
    approximations.
    """
    def update(self, s, y):
        b = y.T.dot(s)
        if b <= 0:
            return

        z = self._hess.dot(s)
        a = s.T.dot(z)
        self._hess += - np.outer(z, z.T) / a + np.outer(y, y.T) / b


class DFP(HessianApproximation):
    """
    Davidon-Fletcher-Powell update strategy. This is a rank 2
    update strategy that always yields positive-semidefinite hessian
    approximations. It usually does not perform as well as the BFGS
    strategy, but included for the sake of completeness.
    """
    def update(self, s, y):
        curv = y.T.dot(s)
        if curv <= 0:
            return
        mat1 = np.eye(self._hess.shape[0]) - np.outer(y, s.T) / curv
        mat2 = np.eye(self._hess.shape[0]) - np.outer(s, y.T) / curv

        self._hess = mat1.dot(self._hess).dot(mat2) + np.outer(y, y.T)/curv


class HybridUpdate(HessianApproximation):
    def __init__(self,
                 happ: HessianApproximation = None,
                 hess_init: Optional[np.ndarray] = None,
                 switch_iteration: Optional[int] = None):
        """
        Create a Hybrid Hessian update strategy which is generated from the
        start but only applied after a certain iteration

        :param happ:
            Hessian Update Strategy (default: BFGS)

        :param switch_iteration:
            Iteration after which this approximation is used (default: 5*dim)

        :param hess_init:
            Initial guess for the Hessian. (default: eye)
        """
        if happ is None:
            happ = BFGS()
        self.hessian_update = happ
        self.switch_iteration = switch_iteration

        super(HybridUpdate, self).__init__(hess_init)

    def init_mat(self, dim: int):
        if self.switch_iteration is None:
            self.switch_iteration = 2*dim
        self.hessian_update.init_mat(dim)

    def update(self, s, y):
        self.hessian_update.update(s, y)

    def get_mat(self) -> np.ndarray:
        return self.hessian_update.get_mat()
