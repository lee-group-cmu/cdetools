import numpy as np
import scipy.stats as stats
from python.cdf_coverage import cdf_coverage


def test__true_density_has_uniform_coverage():
    n_fail = 0
    for _ in range(10):
        np.random.seed(12345)
        n_grid = 1001
        n_test = 73
        z_grid = np.linspace(-5,5,n_grid)
        z_test = np.random.normal(0,1,(n_test,))
        dist = stats.norm()
        cdes = np.array([dist.pdf(z_grid) for _ in range(n_test)]).reshape(n_test, n_grid)
        vals = cdf_coverage(cdes, z_grid, z_test)
        n_fail += 0 if stats.kstest(vals, 'uniform')[1] > 0.01 else 1

    assert n_fail <= 1