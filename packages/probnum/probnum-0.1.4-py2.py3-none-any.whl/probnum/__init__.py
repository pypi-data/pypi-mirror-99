"""ProbNum.

ProbNum implements probabilistic numerical methods in Python. Such methods solve
numerical problems from linear algebra, optimization, quadrature and differential
equations using probabilistic inference. This approach captures uncertainty arising
from finite computational resources and stochastic input.

Available subpackages
---------------------
diffeq
    Probabilistic solvers for ordinary differential equations.
filtsmooth
    Bayesian filtering and smoothing.
kernels
    Kernels / covariance functions.
linalg
    Probabilistic numerical linear algebra.
linops
    Finite-dimensional linear operators.
quad
    Bayesian quadrature / numerical integration.
randvars
    Random variables representing uncertain values.
problems
    Definitions and collection of problems solved by probabilistic numerical methods.
utils
    Utility functions.
"""

from pkg_resources import DistributionNotFound, get_distribution

from . import (
    diffeq,
    filtsmooth,
    kernels,
    linalg,
    linops,
    problems,
    quad,
    randvars,
    statespace,
    utils,
)
from .randvars import RandomVariable, asrandvar

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
