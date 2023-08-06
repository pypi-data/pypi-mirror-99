"""Convenience functions for Gaussian filtering and smoothing.

References
----------
.. [1] https://arxiv.org/pdf/1610.05261.pdf
.. [2] https://arxiv.org/abs/1807.09737
.. [3] https://arxiv.org/abs/1810.03440
.. [4] https://arxiv.org/pdf/2004.00623.pdf
"""

import numpy as np

from probnum import randvars, statespace

from .. import steprule
from ..ode import IVP
from .ivpfiltsmooth import GaussianIVPFilter

__all__ = ["probsolve_ivp"]


def probsolve_ivp(
    f,
    t0,
    tmax,
    y0,
    df=None,
    method="EK0",
    dense_output=True,
    algo_order=2,
    adaptive=True,
    atol=1e-2,
    rtol=1e-2,
    step=None,
):
    r"""Solve initial value problem with Gaussian filtering and smoothing.

    Numerically computes a Gauss-Markov process which solves numerically
    the initial value problem (IVP) based on a system of first order
    ordinary differential equations (ODEs)

    .. math:: \\dot x(t) = f(t, x(t)), \\quad x(t_0) = x_0,
        \\quad t \\in [t_0, T]

    by regarding it as a (nonlinear) Gaussian filtering (and smoothing)
    problem [3]_. For some configurations it recovers certain multistep
    methods [1]_.
    Convergence rates of filtering [2]_ and smoothing [4]_ are
    comparable to those of methods of Runge-Kutta type.


    This function turns a prior-string into an :class:`ODEPrior`, a
    method-string into a filter/smoother of class :class:`GaussFiltSmooth`, creates a
    :class:`GaussianIVPFilter` object and calls the :meth:`solve()` method. For
    advanced usage we recommend to do this process manually which
    enables advanced methods of tuning the algorithm.

    This function supports the methods:
    extended Kalman filtering based on a zero-th order Taylor
    approximation (EKF0),
    extended Kalman filtering (EKF1),
    unscented Kalman filtering (UKF),
    extended Kalman smoothing based on a zero-th order Taylor
    approximation (EKS0),
    extended Kalman smoothing (EKS1), and
    unscented Kalman smoothing (UKS).

    For adaptive step-size selection of ODE filters, we implement the
    scheme proposed by Schober et al. (2019), and further examined by Bosch et al (2021),
    where the local error estimate is derived from the local, calibrated
    uncertainty estimate.

    Arguments
    ---------
    f :
        ODE vector field.
    t0 :
        Initial time point.
    tmax :
        Final time point.
    y0 :
        Initial value.
    df :
        Jacobian of the ODE vector field.
    adaptive :
        Whether to use adaptive steps or not. Default is `True`.
    atol : float
        Absolute tolerance  of the adaptive step-size selection scheme.
        Optional. Default is ``1e-4``.
    rtol : float
        Relative tolerance   of the adaptive step-size selection scheme.
        Optional. Default is ``1e-4``.
    step :
        Step size. If atol and rtol are not specified, this step-size is used for a fixed-step ODE solver.
        If they are specified, this only affects the first step. Optional.
        Default is None, in which case the first step is chosen as :math:`0.01 \cdot |y_0|/|f(t_0, y_0)|`.
    algo_order
        Order of the algorithm. This amounts to choosing the order of integration (``ordint``) of an integrated Brownian motion prior.
        For too high orders, process noise covariance matrices become singular. For IBM, this maximum seems to be :`q=11` (using standard ``float64``).
        It is possible that higher orders may work for you.
        The type of prior relates to prior assumptions about the
        derivative of the solution.
        The higher the order of the algorithm, the faster the convergence, but also, the higher-dimensional (and thus the costlier) the state space.
    method : str, optional
        Which method is to be used. Default is ``EK0`` which is the
        method proposed by Schober et al.. The available
        options are

        ================================================  ==============
         Extended Kalman filtering/smoothing (0th order)  ``'EK0'``
         Extended Kalman filtering/smoothing (1st order)  ``'EK1'``
        ================================================  ==============

        First order extended Kalman filtering and smoothing methods (``EK1``)
        require Jacobians of the RHS-vector field of the IVP.
        That is, the argument ``df`` needs to be specified.
        They are likely to perform better than zeroth order methods in
        terms of (A-)stability and "meaningful uncertainty estimates".
        While we recommend to use correct capitalization for the method string,
        lower-case letters will be capitalized internally.
    dense_output : bool
        Whether we want dense output. Optional. Default is ``True``. For the ODE filter,
        dense output requires smoothing, so if ``dense_output`` is False, no smoothing is performed;
        but when it is ``True``, the filter solution is smoothed.

    Returns
    -------
    solution : KalmanODESolution
        Solution of the ODE problem.

        Can be evaluated at and sampled from at arbitrary grid points.
        Further, it contains fields:

        t : :obj:`np.ndarray`, shape=(N,)
            Mesh used by the solver to compute the solution.
            It includes the initial time :math:`t_0` but not necessarily the
            final time :math:`T`.
        y : :obj:`list` of :obj:`RandomVariable`, length=N
            Discrete-time solution at times :math:`t_1, ..., t_N`,
            as a list of random variables.
            The means and covariances can be accessed with ``solution.y.mean``
            and ``solution.y.cov``.

    See Also
    --------
    GaussianIVPFilter : Solve IVPs with Gaussian filtering and smoothing
    KalmanODESolution : Solution of ODE problems based on Gaussian filtering and smoothing.

    References
    ----------
    .. [1] Schober, M., Särkkä, S. and Hennig, P..
        A probabilistic model for the numerical solution of initial
        value problems.
        Statistics and Computing, 2019.
    .. [2] Kersting, H., Sullivan, T.J., and Hennig, P..
        Convergence rates of Gaussian ODE filters.
        2019.
    .. [3] Tronarp, F., Kersting, H., Särkkä, S., and Hennig, P..
        Probabilistic solutions to ordinary differential equations as
        non-linear Bayesian filtering: a new perspective.
        Statistics and Computing, 2019.
    .. [4] Tronarp, F., Särkkä, S., and Hennig, P..
        Bayesian ODE solvers: the maximum a posteriori estimate.
        2019.


    Examples
    --------
    >>> from probnum.diffeq import logistic, probsolve_ivp
    >>> from probnum import randvars
    >>> import numpy as np

    Solve a simple logistic ODE with fixed steps.

    >>> def f(t, x):
    ...     return 4*x*(1-x)
    >>>
    >>> y0 = np.array([0.15])
    >>> t0, tmax = 0., 1.5
    >>> solution = probsolve_ivp(f, t0, tmax, y0, step=0.1, adaptive=False)
    >>> print(np.round(solution.states.mean, 2))
    [[0.15]
     [0.21]
     [0.28]
     [0.37]
     [0.47]
     [0.57]
     [0.66]
     [0.74]
     [0.81]
     [0.87]
     [0.91]
     [0.94]
     [0.96]
     [0.97]
     [0.98]
     [0.99]]


    Other methods are easily accessible.

    >>> def df(t, x):
    ...     return np.array([4. - 8 * x])
    >>> solution = probsolve_ivp(f, t0, tmax, y0, df=df, method="EK1", algo_order=2, step=0.1, adaptive=False)
    >>> print(np.round(solution.states.mean, 2))
    [[0.15]
     [0.21]
     [0.28]
     [0.37]
     [0.47]
     [0.57]
     [0.66]
     [0.74]
     [0.81]
     [0.87]
     [0.91]
     [0.93]
     [0.96]
     [0.97]
     [0.98]
     [0.99]]

    """

    # Create IVP object
    ivp = IVP(
        timespan=(t0, tmax),
        initrv=randvars.Constant(np.asarray(y0)),
        rhs=f,
        jac=df,
    )

    # Create steprule
    if adaptive is True:
        if atol is None or rtol is None:
            raise ValueError(
                "Please provide absolute and relative tolerance for adaptive steps."
            )
        firststep = step if step is not None else steprule.propose_firststep(ivp)
        stprl = steprule.AdaptiveSteps(firststep=firststep, atol=atol, rtol=rtol)
    else:
        stprl = steprule.ConstantSteps(step)

    # Create solver
    prior = statespace.IBM(
        ordint=algo_order,
        spatialdim=ivp.dimension,
        forward_implementation="sqrt",
        backward_implementation="sqrt",
    )

    if method.upper() not in ["EK0", "EK1"]:
        raise ValueError("Method is not supported.")
    measmod = GaussianIVPFilter.string_to_measurement_model(method, ivp, prior)
    solver = GaussianIVPFilter.construct_with_rk_init(
        ivp, prior, measmod, with_smoothing=dense_output
    )

    return solver.solve(steprule=stprl)
