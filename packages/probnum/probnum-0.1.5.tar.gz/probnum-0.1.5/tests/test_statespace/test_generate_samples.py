import numpy as np
import pytest

import probnum.statespace as pnss
from probnum import randvars


class MockTransition(pnss.Transition):
    """Empty transition object to test the generate() function."""

    # pylint: disable=signature-differs
    def __init__(self, dim):
        super().__init__(input_dim=dim, output_dim=dim)

    def forward_realization(self, realization, **kwargs):
        return randvars.Constant(realization), {}

    def forward_rv(self, rv, **kwargs):
        return rv, {}

    def backward_realization(self, *args, **kwargs):
        raise NotImplementedError

    def backward_rv(self, *args, **kwargs):
        raise NotImplementedError


def times_array():
    return np.arange(0.0, 13.0, 1.0)


def times_single_point():
    return np.array([0.0])


@pytest.mark.parametrize("times", [times_array(), times_single_point()])
@pytest.mark.parametrize("test_ndim", [0, 1, 2])
def test_generate_shapes(times, test_ndim):
    """Output shapes are as expected."""
    mocktrans = MockTransition(dim=test_ndim)
    initrv = randvars.Constant(np.random.rand(test_ndim))
    states, obs = pnss.generate_samples(mocktrans, mocktrans, initrv, times)

    assert states.shape[0] == len(times)
    assert states.shape[1] == test_ndim
    assert obs.shape[0] == len(times)
    assert obs.shape[1] == test_ndim
