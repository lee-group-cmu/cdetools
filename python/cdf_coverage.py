import numpy as np
import scipy.stats as stats


def cdf_coverage(cdes, z_grid, z_test):

    nrow_cde, ncol_cde = cdes.shape
    n_samples = z_test.shape[0]
    n_grid_points = z_grid.shape[0]

    if nrow_cde != n_samples:
        raise ValueError("Number of samples in CDEs should be the same as in z_test."
                         "Currently %s and %s." % (nrow_cde, n_samples))
    if ncol_cde != n_grid_points:
        raise ValueError("Number of grid points in CDEs should be the same as in z_grid."
                         "Currently %s and %s." % (nrow_cde, n_grid_points))

    z_min = np.min(z_grid)
    z_max = np.max(z_grid)
    z_delta = (z_max - z_min)/n_grid_points
    pvals = [z_delta * np.sum(cdes[ii, np.where(z_grid > z_test[ii])[0]]) for ii in range(n_samples)]
    return np.array(pvals)


### TEST
#   np.random.seed(12345)
#   n_grid = 1001
#   n_test = 73
#   z_grid = np.linspace(-5,5,n_grid)
#   z_test = np.random.normal(0,1,(n_test,))
#   dist = stats.norm()
#   cdes = np.array([dist.pdf(z_grid) for _ in range(n_test)]).reshape(n_test, n_grid)
#   pvals = cdf_coverage(cdes, z_grid, z_test)
#   stats.kstest(pvals, 'uniform')