import numpy as np
import scipy.stats as stats

from python.hpd_coverage import hpd_coverage

def test__true_density_uniform_HPD_coverage():
    n_fail = 0
    np.random.seed(12345)
    for _ in range(10):
        n_grid = 1001
        n_test = 73
        z_grid = np.linspace(-5,5,n_grid)
        z_test = np.random.normal(0,1,(n_test,))
        dist = stats.norm()
        cdes = np.array([dist.pdf(z_grid) for _ in range(n_test)]).reshape(n_test, n_grid)
        vals = hpd_coverage(cdes, z_grid, z_test)
        n_fail += 0 if stats.kstest(vals, 'uniform')[1] > 0.01 else 1

    assert n_fail <= 1


def test__true_mult_density_uniform_HPD_coverage():
    n_fail = 0
    np.random.seed(12345)
    for _ in range(10):
        n_grid = 51
        n_test = 701
        xx_grid, yy_grid = np.meshgrid(np.linspace(0, 1, n_grid), np.linspace(0, 1, n_grid))
        z_grid = np.hstack((xx_grid.reshape(-1, 1), yy_grid.reshape(-1,1)))
        z_test = np.hstack((np.random.beta(a=2, b=3, size=(n_test, 1)),
                            np.random.beta(a=4, b=1, size=(n_test, 1))))
        dist_beta1 = stats.beta(2, 3)
        dist_beta2 = stats.beta(4, 1)
        cde = dist_beta1.pdf(z_grid[:, 0]) * dist_beta2.pdf(z_grid[:, 1])
        cdes = np.tile(cde, (n_test, 1))
        vals = hpd_coverage(cdes, z_grid, z_test)
        n_fail += 0 if stats.kstest(vals, 'uniform')[1] > 0.01 else 1

    assert n_fail <= 1