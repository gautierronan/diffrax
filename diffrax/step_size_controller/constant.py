from typing import Optional, Tuple

from ..custom_types import Array, PyTree, Scalar
from ..solution import RESULTS
from ..solver import AbstractSolver
from .base import AbstractStepSizeController


class ConstantStepSize(AbstractStepSizeController):
    """Use a constant step size, equal to the `dt0` argument of
    [`diffrax.diffeqsolve`][].
    """

    def wrap(self, unravel_y: callable, direction: Scalar):
        return self

    def init(
        self,
        t0: Scalar,
        y0: Array["state"],  # noqa: F821
        dt0: Optional[Scalar],
        args: PyTree,
        solver: AbstractSolver,
    ) -> Tuple[Scalar, Scalar]:
        del y0, args, solver
        if dt0 is None:
            raise ValueError(
                "Constant step size solvers cannot select step size automatically; "
                "please pass a value for `dt0`."
            )
        return t0 + dt0, dt0

    def adapt_step_size(
        self,
        t0: Scalar,
        t1: Scalar,
        y0: Array["state"],  # noqa: F821
        y1_candidate: Array["state"],  # noqa: F821
        args: PyTree,
        y_error: Array["state"],  # noqa: F821
        solver_order: int,
        controller_state: Scalar,
    ) -> Tuple[bool, Scalar, Scalar, bool, Scalar, int]:
        del t0, y0, args, y_error, solver_order
        return (
            True,
            t1,
            t1 + controller_state,
            False,
            controller_state,
            RESULTS.successful,
        )
