import numpy as np
from scipy.spatial import KDTree


def hpd_coverage(cdes, z_grid, z_test):
    """
    Calculate coverage based upon HPD regions.

    @param cdes: a numpy array of conditional density estimates;
        each row corresponds to an observation, each column corresponds to a grid
        point
    @param z_grid: a numpy array of the grid points at which cde_estimates is evaluated
    @param z_test: a numpy array of the true z values corresponding to the rows of cde_estimates

    @returns A numpy array of values; under the true generating model
       these are Uniform(0, 1)
    """

    if len(z_test.shape) == 1:
        z_test = z_test.reshape(-1, 1)
    if len(z_grid.shape) == 1:
        z_grid = z_grid.reshape(-1, 1)

    nrow_cde, ncol_cde = cdes.shape
    n_samples, feats_samples = z_test.shape
    n_grid_points, feats_grid = z_grid.shape

    if nrow_cde != n_samples:
        raise ValueError("Number of samples in CDEs should be the same as in z_test."
                         "Currently %s and %s." % (nrow_cde, n_samples))
    if ncol_cde != n_grid_points:
        raise ValueError("Number of grid points in CDEs should be the same as in z_grid."
                         "Currently %s and %s." % (nrow_cde, n_grid_points))

    if feats_samples != feats_grid:
        raise ValueError("Dimensionality of test points and grid points need to coincise."
                         "Currently %s and %s." % (feats_samples, feats_grid))

    z_min = np.min(z_grid, axis=0)
    z_max = np.max(z_grid, axis=0)
    z_delta = np.prod(z_max - z_min) / n_grid_points
    kdtree = KDTree(z_grid)

    vals = np.zeros((n_samples, ))
    for ii in range(n_samples):
        nn_id = kdtree.query(z_test[ii, :])[1]
        vals[ii] = z_delta * np.sum(cdes[ii, np.where(cdes[ii, :] > cdes[ii, nn_id])])

    return vals
