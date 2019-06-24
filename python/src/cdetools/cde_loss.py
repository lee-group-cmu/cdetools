import numpy as np
from scipy.spatial import KDTree


def cde_loss(cde_estimates, z_grid, z_test):
    """
    Calculates conditional density estimation loss on holdout data

    @param cde_estimates: a numpy array where each row is a density
    estimate on z_grid
    @param z_grid: a numpy array of the grid points at which cde_estimates is evaluated
    @param z_test: a numpy array of the true z values corresponding to the rows of cde_estimates

    @returns The CDE loss (up to a constant) for the CDE estimator on
    the holdout data and the SE error
    """

    if len(z_test.shape) == 1:
        z_test = z_test.reshape(-1, 1)
    if len(z_grid.shape) == 1:
        z_grid = z_grid.reshape(-1, 1)

    n_obs, n_grid = cde_estimates.shape
    n_samples, feats_samples = z_test.shape
    n_grid_points, feats_grid = z_grid.shape

    if n_obs != n_samples:
        raise ValueError("Number of samples in CDEs should be the same as in z_test."
                         "Currently %s and %s." % (n_obs, n_samples))
    if n_grid != n_grid_points:
        raise ValueError("Number of grid points in CDEs should be the same as in z_grid."
                         "Currently %s and %s." % (n_grid, n_grid_points))

    if feats_samples != feats_grid:
        raise ValueError("Dimensionality of test points and grid points need to coincise."
                         "Currently %s and %s." % (feats_samples, feats_grid))

    z_min = np.min(z_grid, axis=0)
    z_max = np.max(z_grid, axis=0)
    z_delta = np.prod(z_max - z_min) / n_grid_points

    integrals = z_delta * np.sum(cde_estimates**2, axis=1)

    kdtree = KDTree(z_grid)
    nn_ids = np.array(
        [kdtree.query(z_test[ii, :])[1] for ii in range(n_samples)]).reshape(-1,)
    likeli = cde_estimates[(tuple(np.arange(n_samples)), tuple(nn_ids))]

    losses = integrals - 2 * likeli
    loss = np.mean(losses)
    se_error = np.std(losses, axis=0) / (n_obs ** 0.5)

    return loss, se_error
