"""Definitions and collection of problems solved by probabilistic numerical methods."""

from ._problems import (
    InitialValueProblem,
    LinearSystem,
    QuadratureProblem,
    RegressionProblem,
)

__all__ = [
    "RegressionProblem",
    "InitialValueProblem",
    "LinearSystem",
    "QuadratureProblem",
]

# Set correct module paths. Corrects links and module paths in documentation.
RegressionProblem.__module__ = "probnum.problems"
InitialValueProblem.__module__ = "probnum.problems"
LinearSystem.__module__ = "probnum.problems"
QuadratureProblem.__module__ = "probnum.problems"
