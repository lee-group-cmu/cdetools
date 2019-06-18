import numpy as np
import scipy.stats as stats

def cde_loss(cde_estimates, z_grid, z_test):
    """Calculates conditional density estimation loss on holdout data

    @param cde_estimates: a numpy array where each row is a density
    estimate on z_grid
    @param z_grid: a numpy array of the grid points at which cde_estimates is evaluated
    @param z_test: a numpy array of the true z values corresponding to the rows of cde_estimates

    @returns The CDE loss (up to a constant) for the CDE estimator on
    the holdout data and the SE error
    """

    n_obs, n_grid = cde_estimates.shape

    term1 = np.trapz(cde_estimates ** 2, z_grid.flatten())

    nns = [np.argmin(np.abs(z_grid - z_test[ii])) for ii in range(n_obs)]
    term2 = cde_estimates[range(n_obs), nns]

    loss = np.mean(term1 - 2 * term2)
    se_error = np.std(term1 - 2 * term2, axis=0) / (n_obs**0.5)

    return loss, se_error



### TEST
#' z_grid = np.linspace(0, 1, 99)
#' dist_unif = stats.uniform()
#' z_test = dist_unif.rvs(101)
#   dist = stats.beta(2,2)
#   cdes = np.array([dist.pdf(z_grid) for _ in range(101)]).reshape(101, 99)
#' cde_loss(cde, z_grid, z_test)